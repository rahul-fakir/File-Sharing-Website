<?php

/* Main Woo Content */
	add_action('woocommerce_before_main_content', 'chrs_woo_container_start', 10);
	add_action('woocommerce_after_main_content', 'chrs_woo_container_end', 10);
	
	function chrs_woo_container_start() {
		echo '<div class="container"><div class="content-wrap"><div class="product-single row remove-bottom">';
	}
	function chrs_woo_container_end() {
		echo '</div></div></div>';
	}

/* Product Left Column */
	add_action('woocommerce_before_single_product_summary', 'chrs_woo_product_start', 2);
	add_action('woocommerce_before_single_product_summary', 'chrs_woo_product_end', 40);
	
	function chrs_woo_product_start() {
		echo '<div class="six columns alpha product-left">';
	}
	function chrs_woo_product_end() {
		echo '</div>';
	}
/* change position of add-to-cart on single product **/
	remove_action( 'woocommerce_single_product_summary', 'woocommerce_template_single_add_to_cart', 30 );
	add_action( 'woocommerce_before_single_product_summary', 'woocommerce_template_single_add_to_cart', 35 );
	remove_action( 'woocommerce_single_product_summary', 'woocommerce_template_single_price', 10 );
	add_action('woocommerce_before_single_product_summary', 'woocommerce_template_single_price', 30 );


/** Remove Tabs */
	remove_action( 'woocommerce_after_single_product_summary', 'woocommerce_output_related_products', 20 );
	remove_action( 'woocommerce_single_product_summary', 'woocommerce_template_single_meta', 40 );
	add_filter( 'woocommerce_product_tabs', 'woo_remove_product_tabs', 98 );
	function woo_remove_product_tabs( $tabs ) {
		unset( $tabs['description'] ); // Remove the description tab
		unset( $tabs['reviews'] ); // Remove the reviews tab
		unset( $tabs['additional_information'] ); // Remove the additional information tab
		return $tabs;
	}
	
	remove_action( 'woocommerce_single_product_summary', 'woocommerce_template_single_excerpt', 20);

/** Remove short description if product tabs are not displayed */
	function chrs_reorder_product_page() {
		if ( get_option('woocommerce_product_tabs') == 'false' ) {
			remove_action( 'woocommerce_single_product_summary', 'woocommerce_template_single_excerpt', 20 );
		}
	}
	add_action( 'woocommerce_before_main_content', 'chrs_reorder_product_page' );


/**
 * Ensure cart contents update when products are added to the cart via AJAX
 */
function my_header_add_to_cart_fragment( $fragments ) {
 
    ob_start();
    $count = WC()->cart->cart_contents_count;
?>
			<a class="cart-contents" href="<?php echo WC()->cart->get_cart_url(); ?>" title="<?php _e( 'View your shopping cart' ); ?>">
				<img src="<?php echo get_template_directory_uri(); ?>/images/i-cart-nav.png" />
				<?php if ( $count > 0 ) { ?><span><?php echo $count; ?></span><?php } ?>
			</a>
	
<?php 
    $fragments['a.cart-contents'] = ob_get_clean();
     
    return $fragments;
}
add_filter( 'woocommerce_add_to_cart_fragments', 'my_header_add_to_cart_fragment' );



?>
