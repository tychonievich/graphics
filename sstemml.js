#!/usr/bin/env node

// Pandoc filter to render all math with temml

var pandoc = require('pandoc-filter');
var temml = require('temml');

var RI = pandoc.RawInline;

async function action(elt,format,meta) {

	if (elt.t === 'Math'){
		var [tag, math] = elt.c
		if (tag.t === "DisplayMath")
		{
			return RI("html", temml.renderToString(math, { displayMode : true }))
		} else if (tag.t === "InlineMath"){
			return RI("html", temml.renderToString(math))
		}
	} 
}

pandoc.stdio(action);
