/**
The MIT License (MIT)

Copyright (c) 2014 Phil Hughes

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
**/
(function($) {
  "use strict";
  $.fn.onScreen = function(opts) {
    /**
    * Namespace for plugin
    * @var String
    **/
    var namespace = "onscreen";

    /**
    * Variable to hold ref to this
    * @var Object
    **/
    var $this = this;

    /**
    * Array of all elements
    * @var Array
    **/
    var _el = [];

    /**
    * Defaults
    * @var Object
    **/
    var defaults = {
      visible: undefined,
      continuousVisible: undefined,
      hidden: undefined,
      continuousHidden: undefined
    };

    /**
    * Options extends defaults
    * @var Object
    **/
    var options = $.extend({}, defaults, opts);
    
    /**
    * Calculate if element is on screen or not
    * @return Boolean
    **/
    var isElementOnScreen = function($el, scrollTop) {
      // Get very bottom of element
      var elementBottom = $el.offset().top + $el.outerHeight();

      // Get very top of element
      var elementTop = $el.offset().top - scrollTop;

      if (elementTop <= $(window).height() && (elementBottom - scrollTop) >= 0) {
        // Element is on screen
        return true;
      } else {
        // Element is not screen
        return false;
      }
    };

    /**
    * Scroll function
    **/
    var onScroll = function(e) {
      $.each(_el, function() {
        if (isElementOnScreen($(this), $(window).scrollTop())) {
          // Call visible callback if element was previously hidden
          if ($(this).data(namespace + ":visible") === false || 
              $(this).data(namespace + ":visible") === undefined) {
            if (options.visible !== undefined && typeof options.visible == "function") {
              // Run callback with correct scope
              options.visible.call(this);
            }

            // Trigger event
            $(this).trigger(namespace + ":visible");
          }

          // Is continue visible callback available?
          if (options.continuousVisible !== undefined && typeof options.continuousVisible == "function") {
            // Run callback with correct scope
            options.continuousVisible.call(this);
          }

          // Add some data to the element
          $(this).data(namespace + ":visible", true);
        } else {
          // Only call hidden callback if element was previously visible
          if ($(this).data(namespace + ":visible") === true) {
            if (options.hidden !== undefined && typeof options.hidden == "function") {
              // Run callback with correct scope
              options.hidden.call(this);
            }

            // Trigger event
            $(this).trigger(namespace + ":hidden");
          }

          // Is continue hidden callback available?
          if (options.continuousHidden !== undefined && typeof options.continuousHidden == "function") {
            // Run callback with correct scope
            options.continuousHidden.call(this);
          }

          // Remove data
          $(this).data(namespace + ":visible", false);
        }
      });
    };

    /**
    * Init function
    **/
    var init = function() {
      // Scroll event & trigger initial event
      $(window).on("scroll", onScroll);

      // Loop all elements
      return $this.each(function() {
        _el.push($(this));
        $(window).trigger("scroll");
      });
    };

    // Start plugin
    return init();
  };
}(jQuery));