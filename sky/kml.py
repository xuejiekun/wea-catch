# -*- coding: utf-8 -*-
from lxml import etree
from pykml.factory import KML_ElementMaker as KML


class KmlMaker:

    def __init__(self):
        self.pm_list = []

    def bulid_pm(self, address_name, lng, lat):
        coor = '{},{}'.format(lng, lat)
        pm = KML.Placemark(
            KML.name(address_name),
            KML.Point(
                KML.coordinates(coor)
            )
        )
        self.pm_list.append(pm)
        return pm

    def get_pm_list(self):
        return self.pm_list

    def build_kml(self, filename):
        if self.pm_list:
            # 建立fld
            fld = KML.Folder(self.pm_list[0])
            for pm in self.pm_list[1:]:
                fld.append(pm)
            # 解析fld
            content = etree.tostring(fld, pretty_print=True, )
            with open(filename, 'wb') as fp:
                fp.write(content)
        return self.pm_list


if __name__ == '__main__':
    p = KmlMaker()

    p.bulid_pm('地址1', 113.45678, 22.34567)
    p.bulid_pm('地址2', -113.45678, -22.34567)

    p.build_kml('1.kml')
