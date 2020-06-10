
import linkshare
import secure_linkshareuserdata
browser = linkshare.open(secure_linkshareuserdata.linkshare_user,secure_linkshareuserdata.linkshare_pass,False)

ret = linkshare.getlink(browser,'13526',
    'https://www.pc-koubou.jp/products/detail.php?product_id=723983&pre=bct1873_bnr',
    'https://www.pc-koubou.jp/upload/save_image/style_nj50gu_2150000324700_gallery_01_1003.jpg',
    'aiueo')

print(ret)


