import time
import subprocess
import os.path

from selenium.webdriver.common.by import By
from django.conf import settings

from modules.ui.page_objects.actions.all_actions_page import ATBAllActionsPage
from products.models import Product

def run(*args):
	Product.objects.update(in_economy=False)

	atb_page = ATBAllActionsPage(
								browser = 'undetected' if 'undetected' in args else 'chrome',
        						headless = True if 'headless' in args else False
								)

	atb_page.open("https://www.atbmarket.com/promo/economy")

	try:

	#atb_page.get_current_address_shop('Броди')
		atb_page.close_alco_banner()

		pages = atb_page.get_all_pages()

		for idx in range(len(pages) - 1):

			products = atb_page.get_page_products()
			print(idx + 1, "-" * 62)

			for i in range(1, len(products) -1):

				rating = atb_page.get_rating(i)

				discount = atb_page.get_discount(i)

				desc = atb_page.get_product_description(i)

				price_top = atb_page.get_product_price_top(i)

				price_bottom = atb_page.get_product_price_bottom(i)

				img = atb_page.get_image_link(i)
						
				prod = atb_page.get_product_link(i)

				classes = atb_page.get_article_classes(i)

				available = True if 'catalog-item--not-available' in classes else False

				ends = True if "catalog-item--ends" in classes else False

				#print(i, rating, discount, desc, price_top, price_bottom, img,
				#        prod, available, ends)
				credentials = {
								'rating': rating,
								'discount': discount,
								'name': desc,
								'image': img,
								'link': prod,
								'price_top': price_top,
								'price_bottom': price_bottom,
								'price_statistic': [(time.strftime("%Y/%m/%d", time.localtime()), price_top)],
								'in_economy': True,
								'is_available': available,
								'is_ends': ends,
								}
				product, is_created = Product.objects.update_or_create(name = desc,
																		defaults={
																			'rating': rating,
																			'discount': discount,
																			'image': img,
																			'link': prod,
																			'price_top': price_top,
																			'price_bottom': price_bottom,
																			'in_economy': True,
																			'is_available': available,
																			'is_ends': ends,
																			},
																		create_defaults=credentials)
				if not is_created:
					product.price_statistic.append((time.strftime("%Y/%m/%d", time.localtime()), price_top))
					product.save()
					print(product)
				print("checking if photo is exists  ", img)
				if not os.path.exists(os.path.join(settings.STATICFILES_DIRS[0], img.split("/")[-1])):
						print("photo is not exists  ", img)
						subprocess.run(["wget", 
					 				"-b", f"{img}", 
									"-P", settings.STATICFILES_DIRS[0]])

			pages = atb_page.get_all_pages()
			pages[idx + 1].click()

	except Exception as err:
		print(err.args, err.with_traceback, err.add_note)
		atb_page.close()
