# -*- coding:utf-8 -*-
import os
from PIL import Image

class FilePath:
    def set_file(self, file):
        self.file = file
        self.root = self.file.split('\\')[:-1]
        self.file_name = self.file.split('\\')[-1]
        self.file_name_without_suffix = self.file_name[:self.file_name.index('.')]
        self.suffix = self.file_name[self.file_name.index('.'):]

    def show_attr(self):
        print('root:{}'.format(self.root))
        print('file_name:{}'.format(self.file_name))
        print('file_name_without_suffix:{}'.format(self.file_name_without_suffix))
        print('suffix:{}'.format(self.suffix))


def imgproc(file, action=None, thumb_size=(32,32)):
    f = FilePath()
    f.set_file(file)
    f.show_attr()

    img_size = [160, 128, 64, 32, 16]
    img = Image.open(file)
    w, h = img.size
    print('图片尺寸为:{} x {}.'.format(w, h))

    if action == 'thumb':
        img.thumbnail(thumb_size)
        img.save(os.path.join(*f.root, '{}_thumb{}'.format(f.file_name_without_suffix, f.suffix)))
        print('生成缩略图成功.')

    elif action == 'icon':
        icon_list = []
        for i in img_size:
            out = img.resize((i, i))
            out_name = os.path.join(*f.root, '{}_{}x{}{}'.format(f.file_name_without_suffix, str(i), str(i), '.png'))
            icon_list.append(out_name)
            out.save(out_name)
        icon_name = os.path.join(*f.root, '{}{}'.format(f.file_name_without_suffix, '.ico'))
        os.system('png2ico {} {}'.format(icon_name, ' '.join(icon_list)))
        # print(' '.join(icon_list))
        print('生成icon成功.')

    else:
        pass


if __name__ == '__main__':
    f1 = r'..\img\liu_test.jpg'
    imgproc(f1, 'icon')
