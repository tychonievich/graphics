function Meta(m)
  if m.license == nil then return end
  tmp = table.unpack(m.license).text
  if tmp == 'CC-by' then
    m.license = pandoc.RawInline('html','<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="This work is licensed under a Creative Commons Attribution 4.0 International License" title="This work is licensed under a Creative Commons Attribution 4.0 International License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a>')
  elseif tmp == 'CC-by-nc' then
    m.license = pandoc.RawInline('html','<a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/"><img alt="This work is licensed under a Creative Commons Attribution-NonCommercial 4.0 International License" title="This work is licensed under a Creative Commons Attribution-NonCommercial 4.0 International License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png" /></a>')
  elseif tmp == 'CC-by-nd' then
    m.license = pandoc.RawInline('html','<a rel="license" href="http://creativecommons.org/licenses/by-nd/4.0/"><img alt="This work is licensed under a Creative Commons Attribution-NoDerivatives 4.0 International License" title="This work is licensed under a Creative Commons Attribution-NoDerivatives 4.0 International License" style="border-width:0" src="https://i.creativecommons.org/l/by-nd/4.0/88x31.png" /></a>')
  elseif tmp == 'CC-by-nc-nd' then
    m.license = pandoc.RawInline('html','<a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/4.0/"><img alt="This work is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License" title="This work is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-nd/4.0/88x31.png" /></a>')
  elseif tmp == 'CC-by-sa' then
    m.license = pandoc.RawInline('html','<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License" title="This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a>.')
  elseif tmp == 'CC-by-nc-sa' then
    m.license = pandoc.RawInline('html','<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License" title="This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>')
  end
  return m
end
