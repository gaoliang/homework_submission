/*
 * Title: Textarea developer TAB key (beta)
 * Author: Marco Bonelli (http://stackoverflow.com/users/3889449)
 *
 * Description:
 *   Enables extended TAB functionality on textareas of the current page for indenting/dedenting single/multiple lines.
 *   The default indentation is 4 spaces ("    "); change the var TAB_CHAR if you want to use another TAB delimiter.
 *   Originally developed for Stack Overflow Markdown editor.
 *
 * Implementation:
 *   Use 'element.enableTextareaDev()' to enable the feature for all the textareas inside the element (including the element itself).
 *   Use 'element.disableTextareaDev()' to disable the previously enabled feature.
 *
 * Usage:
 *   Single line: place the cursor where you want and press [TAB] to add a tab character, or [SHIFT]+[TAB] to remove a previously inserted tab character (before the caret position).
 *   Multi line: select multiple lines of code and press [TAB] to add a tab character at the beginning of each line, or [SHIFT]+[TAB] to remove previously inserted tab characters.
 *
 */

(function () {
    function textareaDev(e) {
        var TAB_CHAR = '    ',
            t = e.target,
            ds = 0,
            s, ss, se, v;

        if (t.tagName == 'TEXTAREA' && e.keyCode == 9) {
            e.stopPropagation();
            e.preventDefault();

            ss = t.selectionStart;
            se = t.selectionEnd;
            s = t.value.substring(ss, se);
            v = t.value;

            if (~s.indexOf('\n')) {
                if (e.shiftKey) {
                    s = s.split('\n').map(function (el) {
                        if (el.substr(0, TAB_CHAR.length) == TAB_CHAR) return el.substr(4);
                        return el;
                    }).join('\n');

                    t.value = v.substr(0, ss) + s + v.substr(se);
                } else {
                    s = s.split('\n').map(function (el) {
                        return TAB_CHAR + el
                    }).join('\n');
                    t.value = v.substr(0, ss) + s + v.substr(se);
                }

                t.selectionStart = ss;
                t.selectionEnd = ss + s.length;
            } else {
                if (e.shiftKey) {
                    if (v.substr(ss - TAB_CHAR.length, TAB_CHAR.length) == TAB_CHAR) {
                        t.value = v.substr(0, ss - TAB_CHAR.length) + v.substr(se);
                        ds = -TAB_CHAR.length;
                    }
                } else {
                    t.value = v.substr(0, ss) + TAB_CHAR + v.substr(se);
                    ds = TAB_CHAR.length;
                }

                t.selectionStart = t.selectionEnd = ss + ds;
            }
        }
    }

    Object.defineProperties(Element.prototype, {
        enableTextareaDevTab: {
            value: function () {
                this.addEventListener('keydown', textareaDev, true);
            }
        },
        disableTextareaDevTab: {
            value: function () {
                this.removeEventListener('keydown', textareaDev);
            }
        }
    });

    document.getElementById('content').enableTextareaDevTab();
})();