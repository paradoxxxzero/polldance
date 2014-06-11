// Generated by CoffeeScript 1.7.1
(function() {
  $((function(_this) {
    return function() {
      var color, ctx, last, rd, size, ws;
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
      size = 5 + parseInt(Math.random() * 10);
      last = 0;
      ctx.fillStyle = color;
      ws = new WebSocket("ws://" + location.host + "/ws");
      return ws.onopen = function() {
        var draw, plot;
        ws.onmessage = function(data) {
          var point;
          point = JSON.parse(data.data);
          ctx.fillStyle = point.c;
          ctx.beginPath();
          ctx.arc(parseInt(point.x), parseInt(point.y), point.s, 2 * Math.PI, false);
          return ctx.fill();
        };
        draw = false;
        $(document).mousedown(function(e) {
          return draw = true;
        });
        $(document).mouseup(function(e) {
          draw = false;
          return setTimeout(plot, 1, e);
        });
        $(document).mousemove(function(e) {
          if (draw) {
            return setTimeout(plot, 1, e);
          }
        });
        return plot = function(e) {
          return ws.send(JSON.stringify({
            x: e.clientX,
            y: e.clientY,
            c: color,
            s: size
          }));
        };
      };
    };
  })(this));

}).call(this);