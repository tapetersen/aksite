#coding: utf-8

sections = (
    u"flöjt",
    u"klarinett",
    u"saxofon",
    u"trumpet",
    u"trombon",
    u"komp",
    u"balett"
)
section_choices = [(s[0]+s[-1], s) for s in sections]

instruments = {
    u"flöjt":u"flöjt",
    u"klarinett":u"klarinett",
    u"altsax":u"saxofon",
    u"tenorsax":u"saxofon",
    u"barytonsax":u"saxofon",
    u"trumpet":u"trumpet",
    u"trombon":u"trombon",
    u"tuba":u"komp",
    u"banjo":u"komp",
    u"slagverk":u"komp",
    u"euphonium":u"komp",
    u"horn":u"komp",
    u"balett":u"balett"
}
instrument_choices = [(i[0]+i[-1], i) for i in sorted(instruments.keys())]

instrument_to_short = {instrument:str(short) for short, instrument in instrument_choices}
short_to_instrument = {str(short):instrument for short, instrument in instrument_choices}

section_to_short_instruments = {section:[
        instrument_to_short[instrument] for instrument in instruments 
                if instruments[instrument] == section
        ] for section in sections}
