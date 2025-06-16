function CodeBlock(block)
  if block.classes[1] == "pikchr" then
    local svg = pandoc.pipe("./pikchr", {"--svg-only", "-"}, block.text)
    return pandoc.RawBlock('html', string.gsub(svg,"(viewBox=\"[^ ]* [^ ]* )([^ ]*)","style=\"max-width: calc(%2em / 16)\" %1%2"))
  end
end
function Code(element)
  if element.classes[1] == "pikchr" then
    local svg = pandoc.pipe("./pikchr", {"--svg-only", "-"}, element.text)
    return pandoc.RawInline('html', string.gsub(svg,"(viewBox=\"[^ ]* [^ ]* )([^ ]*)","style=\"vertical-align:middle; width: calc(%2em / 16)\" %1%2"))
  end
end
