// Invoke cmd with a special context about the selection and patterns
// import * as utils from 'lib';

//export
const wrapper_main = {
  callCmd(cmd, beginPattern, endPattern) {
    // Param fetching
    let sel = window.getSelection();
    let node = sel.focusNode;

    let shadowRootSelection = $('.field', node)[0]
    shadowRootSelection = shadowRootSelection && shadowRootSelection.shadowRoot;
    shadowRootSelection = shadowRootSelection && shadowRootSelection.getSelection();
    
    sel = shadowRootSelection || sel;
    node = sel.focusNode;

    if(sel.rangeCount <= 0 || !node)
      return;
    const range = sel.getRangeAt(0);

    // Context creation
    const toSend = {
      sel,
      node,
      range,
      beginPattern,
      endPattern,
      beginIndex: null,
      endIndex: null,
      beginPatternMatch: null,
      endPatternMatch: null,
    };

    // Adding matches of patterns if they exist
    const text = node.textContent.substring(0, range.startOffset) + '\x1f' + node.textContent.substring(range.startOffset);
    const regex = new RegExp("(?<=^.*)(" + beginPattern + ")(?:.(?!" + endPattern + "))*\x1f.*?(" + endPattern + ")", "g");
    const match = regex.exec(text);

    if(match !== null && match.index !== null && match[0] !== null) {
      toSend.beginIndex = match.index;
      toSend.endIndex = match.index + match[0].length - 1;
      toSend.beginPatternMatch = match[1];
      toSend.endPatternMatch = match[2];
    }

    // Done
    cmd(toSend)
  },

  wrapper_lib,
};
