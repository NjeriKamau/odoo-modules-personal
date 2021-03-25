$(document).ready(function(){

    $('#title').ready(function(){
        $.ajax({
            url: '/titles',
            dataType: 'json',
            type: 'post',
            contentType: 'application/json',
            data: JSON.stringify({ "all": true })
        })
        .done(function(data) {
            var opt_str = '';
            for (var i = data['result'].length - 1; i >= 0; i--) {
                opt_str += '<option value='+ data['result'][i].id +'>'+ data['result'][i].name +'</option>';
            };
            $("#title").html(opt_str);
        })
    })

    $('#sector').ready(function(){
        $.ajax({
            url: '/sectors',
            dataType: 'json',
            type: 'post',
            contentType: 'application/json',
            data: JSON.stringify({ "all": true })
        })
        .done(function(data) {
            var opt_str = '';
            for (var i = data['result'].length - 1; i >= 0; i--) {
                opt_str += '<option value='+ data['result'][i].id +'>'+ data['result'][i].name +'</option>';
            };
            $("#sector").html(opt_str);
        })
    })

    $('#country_id').ready(function(){
        $.ajax({
            url: '/country',
            dataType: 'json',
            type: 'post',
            contentType: 'application/json',
            data: JSON.stringify({ "all": true })
        })
        .done(function(data) {
            var opt_str = '';
            for (var i = data['result'].length - 1; i >= 0; i--) {
                opt_str += '<option value='+ data['result'][i].id +'>'+ data['result'][i].name +'</option>';
            };
            $("#country_id").html(opt_str);
        })
    })

});
