import os
import tarfile
from io import BytesIO

import fire
import tqdm

import cv0 as cv2


def 寫tar(tar文件名, 數據表: dict):
    fgz = BytesIO()
    with tarfile.open(mode="w:xz", fileobj=fgz) as tar:
        for i, 數據 in 數據表.items():
            tarinfo = tarfile.TarInfo(name=i)
            f1 = BytesIO(數據)
            tarinfo.size = len(f1.read())
            f1.seek(0)
            tar.addfile(tarinfo, fileobj=f1)
    fgz.seek(0)

    with open(tar文件名, 'wb') as f:
        f.write(fgz.read())


def 輝き(src_path, dst_path='./_output/'):
    源路徑 = src_path
    輸出路徑 = dst_path
    try:
        os.makedirs(輸出路徑)
    except:
        None

    print('整理中……')
    圖片表 = {}
    for 文件名 in tqdm.tqdm(os.listdir(源路徑), ncols=50):
        文件全名 = os.path.join(源路徑, 文件名)
        當前項 = {'文件名': 文件名, '圖': cv2.read(文件全名)}
        for 名, 項目組 in 圖片表.items():
            對照圖 = 項目組[0]['圖']
            if 當前項['圖'].shape == 對照圖.shape and (當前項['圖'] == 對照圖).mean() > 0.3:
                項目組.append(當前項)
                print(f'「{當前項["文件名"]}」與「{名}」融合。')
                break
        else:
            圖片表[文件名] = [當前項]
            print(f'新圖片「{當前項["文件名"]}」')

    print('壓縮中……')
    for 名, 項目組 in tqdm.tqdm(圖片表.items(), ncols=50):
        基名 = os.path.splitext(os.path.basename(名))[0]
        預覽 = 項目組[0]['圖'].copy()
        預覽 = cv2.resize(預覽, (預覽.shape[1] // 2, 預覽.shape[0] // 2))
        cv2.write(預覽, os.path.join(輸出路徑, f'{基名}_預覽.jpg'))
        寫tar(os.path.join(輸出路徑, f'{基名}.tar'),
             {i['文件名']: cv2.imencode('.bmp', i['圖'])[1] for i in 項目組})


if __name__ == '__main__':
    fire.Fire(輝き)
