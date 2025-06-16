local notenum = 0
function Note(elem)
  notenum = notenum + 1
  local anchor = pandoc.RawInline("html", "<label for='sn" .. notenum .. "' class='notemarker'><sup>"..notenum.."</sup></label><input type='checkbox' class='margin-toggle' id='sn"..notenum.."'>")
  local marker = pandoc.Span(pandoc.Superscript(pandoc.Str(notenum)), {class="notemarker"})
  local body = pandoc.utils.blocks_to_inlines(elem.c)
  pandoc.List.insert(body, 1,pandoc.Space())
  pandoc.List.insert(body, 1,marker)
  local wrapped = pandoc.Span(body, {class="sidenote", role="doc-footnote"})
  return pandoc.List({anchor, wrapped})
end
