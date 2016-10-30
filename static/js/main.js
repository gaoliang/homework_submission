// 背景渐变颜色控制
    $('body').gradientify({
    gradients: [
        { start: [49,76,172], stop: [242,159,191] },
        { start: [255,103,69], stop: [240,154,241] },
        { start: [33,229,241], stop: [235,236,117] }
    ]
});

    //瀑布流布局控制
    $('.grid').masonry({
  // set itemSelector so .grid-sizer is not used in layout
  itemSelector: '.grid-item',

  // use element for option
  columnWidth: '.grid-sizer',
  percentPosition: true
})
