<?php
add_filter('widget_text', 'do_shortcode');

function chrs_youtube( $atts ) {
	extract( shortcode_atts( array(
		'video_id' => ' '
	), $atts ) );
	
	ob_start();
		echo '<div class="video-container"><iframe src="http://www.youtube.com/embed/'.$video_id.'" frameborder="0" width="560" height="315"></iframe></div>';
	return ob_get_clean();
}
add_shortcode( 'youtube', 'chrs_youtube' );

function chrs_vimeo( $atts ) {
	extract( shortcode_atts( array(
		'video_id' => ' '
	), $atts ) );
	
	ob_start();
		echo '<div class="video-container"><iframe src="//player.vimeo.com/video/'.$video_id.'?title=0&amp;byline=0&amp;portrait=0&amp;badge=0&amp;color=ffffff" width="500" height="281" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe></div>';
	return ob_get_clean();
}
add_shortcode( 'vimeo', 'chrs_vimeo' );


// Column Layouts
function chrs_col_two( $atts, $content = null ) {
	return '<div class="one-half column first">'.$content.'</div>';
}
add_shortcode('col-2', 'chrs_col_two');

function chrs_col_two_last( $atts, $content = null ) {
	return '<div class="one-half column last">'.$content.'</div><div class="clearer"></div>';
}
add_shortcode('col-2-last', 'chrs_col_two_last');

function chrs_col_three( $atts, $content = null ) {
	return '<div class="one-third column alpha">'.$content.'</div>';
}
add_shortcode('col-3', 'chrs_col_three');

function chrs_col_three_last( $atts, $content = null ) {
	return '<div class="one-third column omega last">'.$content.'</div><div class="clearer"></div>';
}
add_shortcode('col-3-last', 'chrs_col_three_last');


// Custom Journal loop shortcode
function chrs_loop_latest( $atts ) {

	global $wp_query;

	extract(shortcode_atts(array(
		'showposts' 	=> '6',
	), $atts));

	$args = array(
		'post_type'	=> 'post',
		'post_status' => 'publish',
		'showposts' => $showposts
	);

	ob_start();

	$posts = new WP_Query( $args );
	
	 if ( $posts->have_posts() ) : ?>

    <div class="testimonials" id="feat-posts">
        <ul class="slides">
        <?php while ( $posts->have_posts() ) : $posts->the_post(); ?>
            <li class="feat-post">
                <a href="<?php the_permalink();?>"><?php the_post_thumbnail('feat-thumb', array('class' => 'boxed')); ?></a>
                <h3><a href="<?php the_permalink();?>"><?php the_title();?></a></h3>
                <p class="post-meta"><span class="post-author"><?php echo get_the_author();?></span> | <?php the_time('m') ?>.<?php the_time('d') ?>.<?php the_time('Y')?></p>
            </li>
        <?php endwhile; ?>
        </ul>
    </div>
	<?php endif;

	wp_reset_postdata();
	wp_reset_query();

	return ob_get_clean();
}
add_shortcode( 'feat_posts', 'chrs_loop_latest');

// Sidebar Social
function chrs_side_social( $atts, $content = null ) {
	$themeOptions = get_option( 'chrs_theme_options' );
	$fb = $themeOptions['fburl'];
	$pt = $themeOptions['pturl'];
	$tw = $themeOptions['twurl'];
	$li = $themeOptions['liurl'];
	return '
	<ul class="side-social">
		<li><a href="'.$fb.'" target="_blank" class="rounded100"><i class="fa fa-facebook"></i></a></li>
		<li><a href="'.$pt.'" target="_blank" class="rounded100"><i class="fa fa-pinterest"></i></a></li>
		<li><a href="'.$tw.'" target="_blank" class="rounded100"><i class="fa fa-twitter"></i></a></li>
		<li><a href="'.$li.'" target="_blank" class="rounded100"><i class="fa fa-linkedin"></i></a></li>
		<li><a href="https://www.flickr.com/photos/127131247@N05/with/15146109808/" target="_blank" class="rounded100"><i class="fa fa-flickr"></i></a></li>
		<li><a href="'.$ig.'" target="_blank" class="rounded100"><i class="fa fa-instagram"></i></a></li>
	</ul>
	';
}
add_shortcode('side-social', 'chrs_side_social');


?>