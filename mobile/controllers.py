# -*- coding: utf-8 -*-
##############################################################################
#
#    Diogo Carvalho Duarte
#    Copyright (C) 2004-2024 Diogo Duarte (<http://diogocduarte.github.io/>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import http
import openerp
import sys
from openerp.http import request
import werkzeug.utils
import jinja2

if hasattr(sys, 'frozen'):
    # When running on compiled windows binary, we don't have access to package loader.
    path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'views'))
    loader = jinja2.FileSystemLoader(path)
else:
    loader = jinja2.PackageLoader('openerp.addons.mobile', "views")
    
env = jinja2.Environment(loader=loader, autoescape=True)


def login_redirect(redirecturl):
    db = request.session.db
    return http.local_redirect('/mobile/login/%s/%s' % (db, redirecturl[1:]))


class BaseLoginController(http.Controller):

    @http.route(['/mobile/database/selector', '/mobile/database/selector/<path:redirecturl>'], type='http', auth="none")
    def selector(self, redirecturl='mobile/sample', **kw):
        """Returns the database selector using jinja template
            moving to login form for authentication.

           :param redirecturl path: redirection url
           :return: html for selector
        """
        try:
            dbs = http.db_list()
            if not dbs:
                return http.local_redirect('/web/database/manager')
        except openerp.exceptions.AccessDenied:
            dbs = False
        return env.get_template("database_selector.html").render({
            'databases': dbs,
            'debug': request.debug,
            'redirect_url': redirecturl
        })
    
    @http.route('/mobile/login/<string:db>/<path:redirecturl>', type='http', methods=['GET'], auth="none")
    def getlogin(self, db, redirecturl, **kwargs):
        """Coming from database selector will show
            authentication form.

           :param db string: database name
           :param redirecturl path: redirection url
           :return: html for selector
        """
        if not db:
            return http.local_redirect('/mobile/database/selector')
        return http.request.render('mobile.login', {
            'root': '/mobile/',
            'd_db': db,
            'redirect_url': redirecturl
        })
        
    @http.route('/mobile/login/<string:db>', type='http', methods=['POST'], auth="none")
    def postlogin(self, db, **kwargs):
        """Coming from authentication form will
            process the POST request for user authentication.

           :param db string: database name
           :param redirecturl path: redirection url
           :return: html for selector
        """
        values = {}
        wsgienv = request.httprequest.environ
        cr, uid, context, session = request.cr, request.uid, request.context, request.session
        old_uid = uid
        uid = request.session.authenticate(request.session.db, request.params['login'], request.params['password'])
        if uid is not False:
            return werkzeug.utils.redirect(kwargs['redirecturl-f'])
        request.uid = old_uid
        values['error'] = "Wrong login/password"
        values['redirect_url'] = kwargs['redirecturl-f']
        values['d_db'] = kwargs['db1']
        return request.render('mobile.login', values)
    
    @http.route('/mobile/logout/<string:db>/<path:redirecturl>', type='http', methods=['GET'], auth="user")
    def getlogout(self, db, redirecturl, **kwargs):
        request.session.logout(keep_db = True)
        return http.local_redirect('/mobile/login/%s/%s' % (db, redirecturl))
