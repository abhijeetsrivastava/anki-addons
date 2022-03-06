//export
let wrapper_commands = {
  /* Wrap text */
  wrap({beginPattern, endPattern}) {
    wrap(beginPattern, endPattern);
  },

  /* Move to end of pattern */
  moveEnd({sel, endIndex}) {
    wrapper_lib.moveCursor(sel, endIndex);
  },

  /* Move to end of pattern, but inside */
  moveEndInside({sel, endIndex, endPatternMatch}) {
    wrapper_lib.moveCursor(sel, endIndex - endPatternMatch.length);
  },

  /* Move to beginning of pattern */
  moveBegin({sel, beginIndex}) {
    wrapper_lib.moveCursor(sel, beginIndex);
  },

  /* Move to beginning of pattern, but inside */
  moveBeginInside({sel, beginIndex, beginPatternMatch}) {
    wrapper_lib.moveCursor(sel, beginIndex + beginPatternMatch.length);
  },

  /* Destroys selected pattern */
  unwrap({sel, beginIndex, beginPatternMatch, endIndex, endPatternMatch}) {
    wrapper_lib.moveCursor(sel, endIndex - endPatternMatch.length, endIndex);
    setFormat("delete");

    wrapper_lib.moveCursor(sel, beginIndex, beginIndex + beginPatternMatch.length);
    setFormat("delete");
  },
}
