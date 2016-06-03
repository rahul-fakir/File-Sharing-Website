//открытие статистики в кабинете

    function reprintStatisticTop(data)
    {
        $('.tile_count .tile_stats_count .count').text(data.visitor);
    }

    function visitorsOpen(){
      $.ajax({
        url: "/statistic/opensAjax/",
        type: 'POST',
        data: { open: true },
        dataType: "json",
        success: function(data){
            reprintStatisticTop(data);
        },
        errors: function() {

        },
        // CSRF механизм защиты Django
        beforeSend: function(xhr, settings) {
            console.log('-------------before send--');
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
            }
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });// ajax
  };


    function visitorsOpenTime()
    {
        $.ajax({
        url: "/statistic/opensAjax/",
        type: 'POST',
        data: { },
        dataType: "json",
        success: function(data){
            reprintStatisticTop(data);
        },
        errors: function() {

        },
        // CSRF механизм защиты Django
        beforeSend: function(xhr, settings) {
            console.log('-------------before send--');
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
            }
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
          }
        });// ajax
    }


visitorsOpen();

setInterval(visitorsOpenTime, 5000);