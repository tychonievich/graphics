function Table (tbl)
  tbl.colspecs = tbl.colspecs:map(function (colspec)
      local align = colspec[1]
      local width = nil  -- default width
      return {align, width}
  end)
  return tbl
end
