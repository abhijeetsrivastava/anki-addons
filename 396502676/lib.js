// Move the cursor to pos. If end is provided, select the whole text
//export
const wrapper_lib =
{
  moveCursor(sel, pos, end = null) {
    sel.collapse(sel.focusNode, pos);
    if(end !== null)
      sel.extend(sel.focusNode, end);
  },
};
