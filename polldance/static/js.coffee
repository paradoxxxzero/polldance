# Copyright (C) 2011 by Florian Mounier, Kozea
# This file is part of polldance licensed under a 3-clause BSD license.
$ () =>
  $('body').css(margin: 0, padding: 0, overflow: 'hidden')
  $('canvas').css(width: @innerWidth, height: @innerHeight, backgroundColor: 'black')
  ctx = $('canvas').get(0).getContext('2d')
  $('canvas').get(0).width = @innerWidth
  $('canvas').get(0).height = @innerHeight
  rd = () ->
      100 + parseInt(Math.random() * 155)
  color = "rgba(#{rd()}, #{rd()}, #{rd()}, 0.3)"
  size = 5 + parseInt(Math.random() * 10)
  last = 0

  ctx.fillStyle = color

  ws = new WebSocket("ws://#{location.host}/ws")
  ws.onopen = ->

    ws.onmessage = (data) ->
      point = JSON.parse data.data
      ctx.fillStyle = point.c
      ctx.beginPath()
      ctx.arc(parseInt(point.x), parseInt(point.y), point.s, 2 * Math.PI, false)
      ctx.fill()

    draw = false
    $(document).mousedown (e) ->
       draw = true

    $(document).mouseup (e) ->
      draw = false
      setTimeout plot, 1, e

    $(document).mousemove (e) ->
      setTimeout plot, 1, e if draw

    plot = (e) ->
        ws.send JSON.stringify
          x: e.clientX
          y: e.clientY
          c: color
          s: size
