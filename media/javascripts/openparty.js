(function() {
  var FavoriteImages, initialPoster;

  FavoriteImages = ["http://farm9.staticflickr.com/8288/7622028718_1e58ef6ba4.jpg", "http://farm9.staticflickr.com/8160/7621993436_6a4ddbf798.jpg", "http://farm9.staticflickr.com/8018/7622000750_e316cecee8.jpg", "http://farm9.staticflickr.com/8016/7622018536_864fe55437.jpg", "http://farm8.staticflickr.com/7113/7622031186_a4225ccc84.jpg", "http://farm8.staticflickr.com/7117/7622032440_3402f05e3f.jpg", "http://farm8.staticflickr.com/7134/7622033708_922b0190c3.jpg", "http://farm8.staticflickr.com/7259/7622036194_8bf097f926.jpg", "http://farm8.staticflickr.com/7139/7622057492_162643267c.jpg", "http://farm8.staticflickr.com/7248/7622055324_57229a029c.jpg", "http://farm9.staticflickr.com/8286/7622052702_1cb80cbdbf.jpg", "http://farm9.staticflickr.com/8423/7622050296_7634bbef53.jpg", "http://farm9.staticflickr.com/8425/7622047386_c72b879caf.jpg", "http://farm8.staticflickr.com/7275/7622046300_7b24caae73.jpg", "http://farm8.staticflickr.com/7260/7622041802_b5e5e190ed.jpg", "http://farm9.staticflickr.com/8005/7622040522_4960fd70f1.jpg", "http://farm8.staticflickr.com/7127/7622039220_972dbb31ee.jpg", "http://farm9.staticflickr.com/8165/7622059556_44f208ae49.jpg", "http://farm9.staticflickr.com/8145/7622061404_287ee682ef.jpg", "http://farm9.staticflickr.com/8434/7622063824_21c4a66ed7.jpg", "http://farm9.staticflickr.com/8284/7622065486_13313897f0.jpg"];

  initialPoster = function() {
    var $el, nullImageSrc, randomImageSrc;
    nullImageSrc = "/media/images/null.jpg";
    $el = $('#content .poster img');
    if ($el.attr('src') === nullImageSrc) {
      randomImageSrc = _(FavoriteImages).shuffle()[0];
      return $el.attr('src', randomImageSrc);
    }
  };

  $(document).ready(function() {
    return initialPoster();
  });

}).call(this);
