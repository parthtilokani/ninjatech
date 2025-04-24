# -*- coding: utf-8 -*-
from datetime import datetime

from odoo.http import request

import json

from odoo import _

from odoo.addons.website_helpdesk.controllers import main
from odoo.addons.website.controllers import form
from odoo import http, SUPERUSER_ID, _

from werkzeug.exceptions import NotFound
from werkzeug.utils import redirect
from odoo.osv import expression
from odoo.exceptions import ValidationError
import pytz


class WebsiteHelpdesk(main.WebsiteHelpdesk):

    @http.route(['/helpdesk', '/helpdesk/<model("helpdesk.team"):team>'], type='http', auth="public", website=True,
                sitemap=True)
    def website_helpdesk_teams(self, team=None, **kwargs):
        search = kwargs.get('search')

        teams_domain = [('use_website_helpdesk_form', '=', True)]
        if not request.env.user.has_group('helpdesk.group_helpdesk_manager'):
            if team and not team.is_published:
                raise NotFound()
            teams_domain = expression.AND([teams_domain, [('website_published', '=', True)]])

        teams = request.env['helpdesk.team'].search(teams_domain, order="id asc")
        if not teams:
            raise NotFound()

        if not team:
            if len(teams) != 1:
                return request.render("website_helpdesk.helpdesk_all_team", {'teams': teams})
            redirect_url = teams.website_url
            if teams.show_knowledge_base and not kwargs.get('contact_form'):
                redirect_url += '/knowledgebase'
            elif kwargs.get('contact_form'):
                redirect_url += '/?contact_form=1'
            return redirect(redirect_url)

        if team.show_knowledge_base and not kwargs.get('contact_form'):
            return redirect(team.website_url + '/knowledgebase')

        result = self.get_helpdesk_team_data(team or teams[0], search=search)
        category_recs = request.env['helpdesk.category'].sudo().search([])
        result.update({'issues': category_recs})
        print("...................", result)
        result['multiple_teams'] = len(teams) > 1
        return request.render("website_helpdesk.team", result)


class WebsiteForm(main.WebsiteForm):

    def _handle_website_form(self, model_name, **kwargs):
        request.params['partner_id'] = kwargs.get('category_id')
        logged_in_user = request.env.user
        if logged_in_user:
            request.params['partner_id'] = logged_in_user.partner_id.id
            kwargs.update(partner_id=logged_in_user.partner_id.id)
            res = super(WebsiteForm, self)._handle_website_form(model_name, **kwargs)
        return res


class FileTooLargeError(Exception):
    pass

class FileTypeError(Exception):
    pass

def datetime_to_float(dt):
    return dt.hour + dt.minute / 60.0

class SuperWebsiteForm(form.WebsiteForm):
    # Define max file sizes (in bytes)
    MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
    MAX_VIDEO_SIZE = 50 * 1024 * 1024  # 50MB



    def _handle_website_form(self, model_name, **kwargs):
        try:
            return super(SuperWebsiteForm, self)._handle_website_form(model_name, **kwargs)
        except FileTypeError as e:
            return json.dumps({'error': e.args[0]})
        except FileTooLargeError as e:
            # Handle your custom exception and return a custom JSON response
            return json.dumps({'error': e.args[0]})

    def extract_data(self, model, values):
        # Use the super method's return value, which includes attachments set as an empty list
        user_tz = values.pop('user_timezone')
        user_tz = user_tz and user_tz.split(',')[0]
        # add scheduled dates to o2m field
        groups = {}
        keys_to_remove = []  # List to keep track of keys to delete later

        for key, value in values.items():
            # Check if the key matches one of our expected prefixes
            if key.startswith("time_from_") or key.startswith("time_to_") or key.startswith('date_'):
                # Get the suffix number (as string)
                suffix = key.split("_")[-1]
                groups.setdefault(suffix, {})[key] = value
                keys_to_remove.append(key)

        # Remove keys after looping to avoid modifying dictionary while iterating
        for key in keys_to_remove:
            values.pop(key, None)

        # Build the list of tuples, sorted by the suffix (converted to int for numerical order)
        result = []
        for suffix in sorted(groups, key=lambda x: int(x)):
            group = groups[suffix]

            user_timezone = pytz.timezone(user_tz)

            date = datetime.strptime(group.get("date_" + suffix), "%m/%d/%Y")

            from_time = datetime.strptime(group.get("time_from_" + suffix), "%I:%M:%S %p")
            dt_with_tz = user_timezone.localize(from_time)
            # from_time = dt_with_tz.astimezone(pytz.utc)
            # from_time = from_time.replace(tzinfo=None)

            to_time = datetime.strptime(group.get("time_to_" + suffix), "%I:%M:%S %p")
            dt_with_tz = user_timezone.localize(to_time)
            # to_time = dt_with_tz.astimezone(pytz.utc)
            # to_time = to_time.replace(tzinfo=None)
            result.append((0, 0, {'from_time': datetime_to_float(from_time),
                                  'to_time': datetime_to_float(to_time),
                                  'date': date
                                  }))

        data = super(SuperWebsiteForm, self).extract_data(model, values)
        if model.sudo().model == 'helpdesk.ticket':
            validated_attachments = []
            # category_value = data['record'].get('category_id', '')
            # category_rec = False
            # if category_value:
            #     category_rec = request.env['helpdesk.category'].search([('id', '=', int(category_value))], limit=1)
            data['record'].update({'scheduled_slot_ids': result})
            # data['record'].update({
            #     'name': category_rec and category_rec.name or ''
            # })

            # Loop on the attachments already in the super return value.
            for file_obj in data.get('attachments', []):
                # We assume that each attachment has a 'filename' attribute.
                if hasattr(file_obj, 'filename'):
                    file_name = file_obj.filename.lower()
                    max_size, ftype = None, None
                    if file_name.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                        max_size, ftype = self.MAX_IMAGE_SIZE, 'image'
                    elif file_name.endswith(('.mp4', '.avi', '.mov')):
                        max_size, ftype = self.MAX_VIDEO_SIZE, 'video'
                    else:
                        raise FileTypeError(_(
                            "Unsupported file type: %s. Only image and video files are allowed."
                        ) % file_obj.filename)

                    # Validate the file size if applicable.
                    if max_size:
                        pos = file_obj.stream.tell()
                        file_obj.stream.seek(0, 2)
                        size = file_obj.stream.tell()
                        file_obj.stream.seek(pos)
                        if size > max_size:
                            raise FileTooLargeError(_(
                                "%s '%s' is %.2f MB (Max %.2f MB)."
                            ) % (ftype, file_obj.filename, size / (1024 * 1024.0), max_size / (1024 * 1024.0)))
                validated_attachments.append(file_obj)
            # Update the super data with the validated attachments.
            data['attachments'] = validated_attachments
        return data

    # def validate_image(self, attachment):
