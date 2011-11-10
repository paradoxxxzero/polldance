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
    last = 0

    ctx.fillStyle = color

    plot = (data) ->
        ctx.fillStyle = data.c
        ctx.beginPath()
        ctx.arc(parseInt(data.x), parseInt(data.y), 8, 2 * Math.PI, false)
        ctx.fill()

    draw = false
    $(document).mousedown (e) ->
        draw = true

    $(document).mouseup (e) ->
        draw = false

    $(document).mousemove (e) ->
        if draw
            $.ajax
                url: '/set'
                type: 'POST'
                data:
                    x: e.clientX
                    y: e.clientY
                    c: color
                dataType: 'json'

    update = () ->
        $.ajax
            url: "/get/#{last}"
            dataType: 'json'
            success: (data) ->
                last = data.last
                for point in data.points
                    plot point
                setTimeout(update, 50)

    update()
