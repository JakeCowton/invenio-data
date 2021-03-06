# -*- coding: utf-8 -*-
#
## This file is part of Invenio.
## Copyright (C) 2012, 2013, 2014 CERN.
##
## Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

from invenio.config import CFG_SITE_NAME
from fixture import DataSet


class CollectionData(DataSet):

    class siteCollection:
        id = 1
        name = CFG_SITE_NAME
        dbquery = None


    class CMS(siteCollection):
        id = 2
        name = 'CMS'
        dbquery = '980:"CMS"'
        names = {('en', 'ln'): u'CMS Data Analyses',
                 ('fr', 'ln'): u'CMS Data Analyses'}


    class LHCb(siteCollection):
        id = 3
        name = 'LHCb'
        dbquery = '980:"LHCB"'
        names = {('en', 'ln'): u'LHCb Data Analyses',
                 ('fr', 'ln'): u'LHCb Data Analyses'}


    class ALICE(siteCollection):
        id = 4
        name = 'ALICE'
        dbquery = '980:"ALICE"'
        names = {('en', 'ln'): u'ALICE Data Analyses',
                 ('fr', 'ln'): u'ALICE Data Analyses'}
