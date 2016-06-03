<?php
remove_action( 'wp_head', 'feed_links_extra', 3 );
remove_action( 'wp_head', 'rsd_link');
remove_action( 'wp_head', 'index_rel_link');
remove_action( 'wp_head', 'parent_post_rel_link');
remove_action( 'wp_head', 'start_post_rel_link');
remove_action( 'wp_head', 'adjacent_posts_rel_link');
remove_action( 'wp_head', 'wp_generator');

// admin footer text/link
function custom_admin_footer() {
	echo 'Powered by <a href="http://www.wordpress.org" target="_blank">Wordpress</a> | Developed by <a href="http://www.chrsinteractive.com/" target="_blank">CHRS Interactive</a>';
} 
add_filter('admin_footer_text', 'custom_admin_footer');

// admin login logo - 80px 80px
function custom_login_logo() {
	echo '<style type="text/css">
	h1 a { background-image: url('.get_bloginfo('template_directory').'/images/login-logo.png) !important; }
	</style>';
}
add_action('login_head', 'custom_login_logo');

/* WordPress Change Login page logo link */
function change_login_page_url( $url ) {
    return 'http://www.chrsinteractive.com';
}
add_filter( 'login_headerurl', 'change_login_page_url' );

// changing the login page URL hover text
function change_login_page_title(){
return ('Back to Home page'); // changing the title from "Powered by WordPress" to whatever you wish
}
add_filter('login_headertitle', 'change_login_page_title');

// Remove login error message
add_filter('login_errors',create_function('$a', "return null;"));

// Add CHRS Admin bar link
function chrs_admin_bar_link() {
	global $wp_admin_bar;
	if ( !is_super_admin() || !is_admin_bar_showing() )
		return;
	$wp_admin_bar->add_menu( array(
	'id' => 'chrs_link',
	'title' => __( 'WordPress Support'),
	'href' => __('http://www.chrsinteractive.com'),
	) );
}
add_action('admin_bar_menu', 'chrs_admin_bar_link',95);


add_action( 'after_setup_theme', 'woocommerce_support' );
function woocommerce_support() {
	add_theme_support( 'woocommerce' );
} 

?>