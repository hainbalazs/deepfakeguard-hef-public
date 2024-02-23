<template>
    <div class="chart">
        <div :class="['bar', 'bar-' + value, 'cyan', 'lightGray-face']">
            <div class="face top">
                <div class="growing-bar"></div>
            </div>
            <div class="face side-0">
                <div class="growing-bar"></div>
            </div>
            <div class="face floor">
                <div class="growing-bar"></div>
            </div>
            <div class="face side-a"></div>
            <div class="face side-b"></div>
            <div class="face side-1">
                <div class="growing-bar"></div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
  name: "FancyProgressBar",
  props: {
    value: {
      type: Number,
      required: true,
    },
  },

}
</script>

<style lang="scss" scoped>
@use "sass:math";

$yellow: #f1c40f;
$lime: #76c900;
$navy: #0a4069;
$cyan: #57caf4;
$red: #ec008c;
$white: #fefefe;
$gray: #444;
$lightGray: lighten($gray, 30);

$transitionDuration: .3s;
$transition: all $transitionDuration ease-in-out;
$size: 0.8em;

.chart
{
    font-size: $size;

    perspective: 300px;
    perspective-origin: 50% 50%;
    backface-visibility: visible;
}

$faceColor: rgba($white, .3);
$growColor: rgba($red, .6);

.bar
{
    font-size: $size;

    position: relative;

    height: calc(10 * $size);

    transition: $transition;
    transform: rotateX(60deg) rotateY(0deg);

    transform-style: preserve-3d;

    .face
    {
        font-size: calc(2*$size);

        position: relative;

        width: 100%;
        height: calc(2*$size);

        background-color: $faceColor;

        &.side-a,
        &.side-b
        {
            width: calc(2*$size);
        }
    }
    .side-a
    {
        transform: rotateX(90deg) rotateY(-90deg) translateX(calc(2*$size)) translateY(calc(1*$size)) translateZ(calc(1*$size));
    }
    .side-b
    {
        transform: rotateX(90deg) rotateY(-90deg) translateX(calc(4*$size)) translateY(calc(1*$size)) translateZ(calc(-1*$size));
        position: absolute;
        right: 0;
    }
    .side-0
    {
        transform: rotateX(90deg) rotateY(0) translateX(0) translateY(calc(1*$size)) translateZ(calc(-1*$size));
    }
    .side-1
    {
        transform: rotateX(90deg) rotateY(0) translateX(0) translateY(calc(1*$size)) translateZ(calc(3*$size));
    }
    .top
    {
        transform: rotateX(0deg) rotateY(0) translateX(0em) translateY(calc(4*$size)) translateZ(calc(2*$size));
    }
    .floor
    {
        box-shadow: 0 calc(0.1*$size) calc(0.6*$size) rgba(0,0,0,.3), calc(0.6*$size) calc(-0.5*$size) calc(3*$size) rgba(0,0,0,.3), $size calc(-1*$size) calc(8*$size) $white;
    }
}

.growing-bar
{
    transition: $transition;
    background-color: $growColor;
    width: 100%;
    height: calc(2*$size);
}

@mixin drawSkin($color, $name)
{
    .bar.#{$name}
    {
        .side-a,
        // &.bar-100 .side-b,
        .growing-bar
        {
            background-color: rgba($color, .6);
        }
        .side-0 .growing-bar
        {
            box-shadow: calc(-0.5*$size) calc(-1.5*$size) calc(4*$size) $color;
        }
        .floor .growing-bar
        {
            box-shadow: 0em 0em calc(2*$size) $color;
        }
    }
}

@mixin drawFaces($color, $name)
{
    .chart .bar.#{$name} .face
    {
        background-color: rgba($color, .2);
    }
}

@include drawSkin(rgba($yellow, .8), 'yellow');
@include drawSkin(rgba($red, .8), 'red');
@include drawSkin($cyan, 'cyan');
@include drawSkin(rgba($navy, .8), 'navy');
@include drawSkin($lime, 'lime');
@include drawSkin($white, 'white');
@include drawSkin($gray, 'gray');

@include drawFaces(rgba($yellow, .6), 'yellow-face');
@include drawFaces($lime, 'lime-face');
@include drawFaces(rgba($red, .6), 'red-face');
@include drawFaces(rgba($navy, .6), 'navy-face');
@include drawFaces($cyan, 'cyan-face');
@include drawFaces($gray, 'gray-face');
@include drawFaces($lightGray, 'lightGray-face');

@for $i from 0 to 101
{
    .bar-#{$i}
    {
        .growing-bar
        {
            width: percentage(math.div($i, 100));
        }
    }
}


</style>