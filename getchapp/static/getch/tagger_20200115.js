var pos = {
  x: 0,
  y: 0,
  brand_id: undefined,
  item_id: undefined,
  state: 'tag-hidden' // tag-watchable, taggable
};

$('#canvas').on({
  'click': function(e) {
    if (pos.state=='tag-hidden') {
      $('#tags-control').prop('checked', true);
      pos.state = 'tag-watchable';

    } else if (pos.state=='tag-watchable') {
      $('#tags-control').prop('checked', false);
      pos.state = 'tag-hidden';

    } else if (pos.state=='taggable') {
      set_position(e);
      init_tagger();

      $('#cursor').css({ left: pos.x + '%', top: pos.y + '%' });
      $('#cursor-control').prop('checked', true);

      $('#publisher').css({ top: 'calc(' + pos.y + '% - 60px)' });
      $('#publisher .prompt').val('');
      $('#publisher-control').prop('checked', true);

      // time delay 없이 포커스를 주면 안된다. prompt가 뜨는 시간을 고려해야되는 것 같다
      setTimeout(function() { $('#publisher .prompt').focus(); }, 100);
    }
  },
});


function init_tagger() {
  $('#cursor-control').prop('checked', false);
  $('#publisher-control').prop('checked', false);
  $('#brandtag-control').prop('checked', false);
  $('#itemtag-control').prop('checked', false);
}

function init_tagon() {
  $('#tagon-control').prop('checked', false);
  $('#tags-control').prop('checked', false);
}


function set_position(e) {
  var canvas_position = $(e.target).offset();
  var canvas_left = canvas_position.left;
  var canvas_top = canvas_position.top;
  var canvas_width = $(e.target).width();
  var canvas_height = $(e.target).height();

  var page_x = e.pageX;
  var page_y = e.pageY;

  pos.x = (page_x - canvas_left) / canvas_width * 100;
  pos.y = (page_y - canvas_top) / canvas_height * 100;
}


function set_brand(brand_id, image) {
  pos.brand_id = brand_id;
  $('#brandtag img').attr('src', image);
  $('#brandtag-control').prop('checked', true);
}


function set_item(item_id, image) {
  pos.item_id = item_id;
  $('#itemtag img').attr('src', image);
  $('#itemtag-control').prop('checked', true);
}


$('#undo').click(function() {
  if ($('#itemtag-control').prop('checked')) {
    $('#itemtag-control').prop('checked', false);

  } else if ($('#brandtag-control').prop('checked')) {
    $('#brandtag-control').prop('checked', false);

  } else {
    $('#publisher-control').prop('checked', false);
  };
});


$('#editor textarea').on({
  'focusin': function() {
    this.style.height = '40px';
    this.style.height = (this.scrollHeight) + 'px';
  },

  'focusout': function() {
    if (this.value=='') {
      this.style.height = '40px';
    };
  },

  'input': function() {
    this.style.height = '40px';
    this.style.height = (this.scrollHeight) + 'px';
  }
});


function imgerr(img) {
  $(img).css('display', 'none');
}


function load_img(input) {
  if (input.files && input.files[0]) {
    let reader = new FileReader();

    reader.onload = function(e) {
      let img = $(input).next().children('img');
      img.attr("src", e.target.result);
      img.parent().css("display", "block");
    }

    reader.readAsDataURL(input.files[0]);
  }
}


var tagon_drag_stime;
$('#tagon')
  .draggable({
    containment: 'parent', // 부모요소 안에 종속
    opacity: 0.5,
  })
  .on({
    'dragstart': function(event, ui) {
      tagon_drag_stime = Date.now();
    },
    'dragstop': function(event, ui) {
      // 터치 click이 drag로 오인되는 경우를 체크
      if ((Date.now()-tagon_drag_stime) < 200) {
        $(this).trigger('click');
      }
    },
    'click': function() {
      if (pos.state=='taggable') {
        init_tagger();
        init_tagon();
        pos.state = 'tag-hidden';

      } else {
        $('#tagon-control').prop('checked', true);
        pos.state = 'taggable';
      }
    },
    'touchstart': function() {
      $(this).trigger('dragstart');
    }
  });


$('#editor .cancel.button').click(function() {
  init_tagger();
});



function tag_save(save_button) {
  var spinner = new Spinner().spin(document.body);
  $('#editor input[name="x"]').attr('value', pos.x);
  $('#editor input[name="y"]').attr('value', pos.y);
  $('#editor input[name="brand_id"]').attr('value', pos.brand_id);
  $('#editor input[name="item_id"]').attr('value', pos.item_id);

  let formData = new FormData($(save_button).closest('form')[0]);

  $.ajax({
    url: '/channel/tag/save/',
    type: 'POST',
    data: formData,
    // dataType:'json',
    cache: false,
    contentType: false,
    processData: false,
    success: function(data) {
      $('#tags').html(data);
      init_tagger();
    },
    error: function(xhr, errmsg, err) {
      console.log(xhr.status + ': ' + xhr.responseText);
    },
    complete: function() {
      spinner.stop();
    }
  });
}


function post_save(save_button) {
  var spinner = new Spinner().spin(document.body);
  let formData = new FormData($(save_button).closest('form')[0]);

  $.ajax({
    url: '/channel/post/save/',
    type: 'POST',
    data: formData,
    cache: false,
    contentType: false,
    processData: false,
    success: function(data) {
      console.log(data);
      $('#posts').html(data);
    },
    error: function(xhr, errmsg, err) {
      console.log(xhr.status + ': ' + xhr.responseText);
    },
    complete: function() {
      spinner.stop();
    }
  });
}


function load_tagfeeds(ch_id) {
  var spinner = new Spinner().spin(document.body);

  $.ajax({
    url: '/channel/' + ch_id + '/tagfeeds/',
    type: 'GET',
    data: {},
    cache: false,
    contentType: false,
    processData: false,
    success: function(data) {
      $('#tagfeeds').html(data);
    },
    error: function(xhr, errmsg, err) {
      console.log(xhr.status + ': ' + xhr.responseText);
    },
    complete: function() {
      spinner.stop();
    }
  });
}


// function show_feeder() {
//   const commenting = $('#feeder-control').prop('checked');
//   if (commenting) {
//     $('#feeder-control').prop('checked', false);
//
//   } else {
//     $('#feeder-control').prop('checked', true);
//   }
// }
