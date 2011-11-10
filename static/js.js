(function() {
  var _this = this;

  $(function() {
    var color, ctx, draw, last, plot, rd, update;
    $('body').css({
      margin: 0,
      padding: 0,
      overflow: 'hidden'
    });
    $('canvas').css({
      width: _this.innerWidth,
      height: _this.innerHeight,
      backgroundColor: 'black'
    });
    ctx = $('canvas').get(0).getContext('2d');
    $('canvas').get(0).width = _this.innerWidth;
    $('canvas').get(0).height = _this.innerHeight;
    rd = function() {
      return 100 + parseInt(Math.random() * 155);
    };
    color = "rgba(" + (rd()) + ", " + (rd()) + ", " + (rd()) + ", 0.3)";
    last = 0;
    ctx.fillStyle = color;
    plot = function(data) {
      ctx.fillStyle = data.c;
      ctx.beginPath();
      ctx.arc(parseInt(data.x), parseInt(data.y), 8, 2 * Math.PI, false);
      return ctx.fill();
    };
    draw = false;
    $(document).mousedown(function(e) {
      return draw = true;
    });
    $(document).mouseup(function(e) {
      return draw = false;
    });
    $(document).mousemove(function(e) {
      if (draw) {
        return $.ajax({
          url: '/set',
          type: 'POST',
          data: {
            x: e.clientX,
            y: e.clientY,
            c: color
          },
          dataType: 'json'
        });
      }
    });
    update = function() {
      return $.ajax({
        url: "/get/" + last,
        dataType: 'json',
        success: function(data) {
          var point, _i, _len, _ref;
          last = data.last;
          _ref = data.points;
          for (_i = 0, _len = _ref.length; _i < _len; _i++) {
            point = _ref[_i];
            plot(point);
          }
          return setTimeout(update, 50);
        }
      });
    };
    return update();
  });

}).call(this);
