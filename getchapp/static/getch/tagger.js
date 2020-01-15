var pos = {
  x: 0,
  y: 0,
  brand_id: undefined,
  item_id: undefined,
  state: 'tag-hidden' // tag-watchable, taggable
};

$('#canvas').on({
  'click': function(e) {
    set_position(e);
    publisher('hide');
    brandtag('hide');
    itemtag('hide')

    if (pos.state=='tag-hidden') {
      tagon('show');
      tags('show');
      pos.state = 'tag-watchable';

    } else if (pos.state=='tag-watchable') {
      tagon('hide');
      tags('hide');
      pos.state = 'tag-hidden';
    }
  },
});


function set_position(e) {
  let canvas = $('#canvas');
  let canvas_position = canvas.offset();
  let canvas_left = canvas_position.left;
  let canvas_top = canvas_position.top;
  let canvas_width = canvas.width();
  let canvas_height = canvas.height();

  let page_x = e.pageX;
  let page_y = e.pageY;

  pos.x = (page_x - canvas_left) / canvas_width * 100;
  pos.y = (page_y - canvas_top) / canvas_height * 100;
}


function publisher(mode) {
  if (mode=='hide') {
    $('#publisher-show').prop('checked', false);
  } else if (mode=='show') {
    $('#publisher .prompt').val('');
    $('#publisher-show').prop('checked', true);
  }
}

function brandtag(mode) {
  if (mode=='hide') {
    $('#brandtag-show').prop('checked', false);
  } else if (mode=='show') {
    $('#brandtag-show').prop('checked', true);
  }
}

function itemtag(mode) {
  if (mode=='hide') {
    $('#itemtag-show').prop('checked', false);
  } else if (mode=='show') {
    $('#itemtag-show').prop('checked', true);
  }
}

function tags(mode) {
  if (mode=='hide') {
    $('#tags-show').prop('checked', false);
  } else if (mode=='show') {
    $('#tags-show').prop('checked', true);
  }
}

function tagon(mode) {
  if (mode=='hide') {
    $('#tagon-show').prop('checked', false);
    $('#tagon-running').prop('checked', false);
  } else if (mode=='show') {
    $('#tagon').css({ left: 'calc(' + pos.x + '% - 25px)', top: 'calc(' + pos.y + '% - 25px)' });
    $('#tagon-show').prop('checked', true);
    $('#tagon-running').prop('checked', false);
  } else if (mode='running') {
    $('#tagon-show').prop('checked', true);
    $('#tagon-running').prop('checked', true);
  }
}

function set_brand(brand_id, image) {
  pos.brand_id = brand_id;
  $('#brandtag img').attr('src', image);
  brandtag('show');
}

function set_item(item_id, image) {
  pos.item_id = item_id;
  $('#itemtag img').attr('src', image);
  itemtag('show');
}


$('#undo').click(function() {
  if ($('#itemtag-show').prop('checked')) {
    itemtag('hide');
  } else if ($('#brandtag-show').prop('checked')) {
    brandtag('hide');
  } else {
    publisher('hide');
    tagon('hide');
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
    'click': function(e) {
      set_position(e);
      tagon('running');
      publisher('show');

      // time delay 없이 포커스를 주면 안된다. prompt가 뜨는 시간을 고려해야되는 것 같다
      setTimeout(function() { $('#publisher .prompt').focus(); }, 100);
    },
    'touchstart': function() {
      $(this).trigger('dragstart');
    }
  });


$('#editor .cancel.button').click(function() {
  publisher('hide');
  brandtag('hide');
  itemtag('hide');
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
      // console.log(data)
      publisher('hide');
      brandtag('hide');
      itemtag('hide');
      tagon('hide');
      $('#tags').html(data);
      $('#tags .selected.tag .tag-body').trigger('click');
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
