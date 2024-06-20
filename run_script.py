from selenium.webdriver.common.by import By
from modules.ui.page_objects.actions.all_actions_page import ATBAllActionsPage
from products.models import Product
import time

def run():

	atb_page = ATBAllActionsPage()

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

				print(i, rating, discount, desc, price_top, price_bottom, img,
					prod, available, ends)
				credentials = {
					 			'rating': rating,
					 			'discount': discount,
					 			'name': desc,
					 			'image': img,
					 			'link': prod,
					 			'price_top': price_top,
					 			'price_bottom': price_bottom,
					 			'price_statistic': [(time.strftime("%Y/%m/%d", time.localtime()), price_top)],
					 			'is_availabe': available,
					 			'is_ends': ends,
															}
				product, is_exists = Product.objects.update_or_create(name = desc,
																		  defaults={
																			   'is_available': available,
																			   'is_ends': ends,
																			   },
																		  create_defaults=credentials)
				if not is_exists:
					product.price_statistic.append((time.strftime("%Y/%m/%d", time.localtime()), price_top))
					product.save()

			pages= atb_page.get_all_pages()
			pages[idx + 1].click()

	except Exception as err:
		print(err.args, err.with_traceback, err.add_note)
		atb_page.close()

		 

if __name__ == '__main__':
		run()