csvSource := $(wildcard source/*.csv)

# csv2table
csv2tableMdSource := $(patsubst source/%.csv,csv2table/%.source.md,$(csvSource))
csv2tableNative := $(patsubst source/%.csv,csv2table/%.native,$(csvSource))
csv2tableMdTarget := $(patsubst source/%.csv,csv2table/%.target.md,$(csvSource))
csv2tableHtml := $(patsubst source/%.csv,csv2table/%.html,$(csvSource))
csv2tableTex := $(patsubst source/%.csv,csv2table/%.tex,$(csvSource))
csv2tablePdf := $(patsubst source/%.csv,csv2table/%.pdf,$(csvSource))
csv2table:= $(csv2tableMdSource) $(csv2tableNative) $(csv2tableMdTarget) $(csv2tableHtml) $(csv2tableTex) $(csv2tablePdf)
# placetable
placetableMdSource := $(patsubst source/%.csv,placetable/%.source.md,$(csvSource))
placetableNative := $(patsubst source/%.csv,placetable/%.native,$(csvSource))
placetableMdTarget := $(patsubst source/%.csv,placetable/%.target.md,$(csvSource))
placetableHtml := $(patsubst source/%.csv,placetable/%.html,$(csvSource))
placetableTex := $(patsubst source/%.csv,placetable/%.tex,$(csvSource))
placetablePdf := $(patsubst source/%.csv,placetable/%.pdf,$(csvSource))
placetable := $(placetableMdSource) $(placetableNative) $(placetableMdTarget) $(placetableHtml) $(placetableTex) $(placetablePdf)
# panflute csv-tables
panfluteCsvTablesMdSource := $(patsubst source/%.csv,panflute-csv-tables/%.source.md,$(csvSource))
panfluteCsvTablesNative := $(patsubst source/%.csv,panflute-csv-tables/%.native,$(csvSource))
panfluteCsvTablesMdTarget := $(patsubst source/%.csv,panflute-csv-tables/%.target.md,$(csvSource))
panfluteCsvTablesHtml := $(patsubst source/%.csv,panflute-csv-tables/%.html,$(csvSource))
panfluteCsvTablesTex := $(patsubst source/%.csv,panflute-csv-tables/%.tex,$(csvSource))
panfluteCsvTablesPdf := $(patsubst source/%.csv,panflute-csv-tables/%.pdf,$(csvSource))
panfluteCsvTables := $(panfluteCsvTablesMdSource) $(panfluteCsvTablesNative) $(panfluteCsvTablesMdTarget) $(panfluteCsvTablesHtml) $(panfluteCsvTablesTex) $(panfluteCsvTablesPdf)
# python terminaltables
terminaltablesMdSource := $(patsubst source/%.csv,terminaltables/%.source.md,$(csvSource))
terminaltablesNative := $(patsubst source/%.csv,terminaltables/%.native,$(csvSource))
terminaltablesMdTarget := $(patsubst source/%.csv,terminaltables/%.target.md,$(csvSource))
terminaltablesHtml := $(patsubst source/%.csv,terminaltables/%.html,$(csvSource))
terminaltablesTex := $(patsubst source/%.csv,terminaltables/%.tex,$(csvSource))
terminaltablesPdf := $(patsubst source/%.csv,terminaltables/%.pdf,$(csvSource))
terminaltables := $(terminaltablesMdSource) $(terminaltablesNative) $(terminaltablesMdTarget) $(terminaltablesHtml) $(terminaltablesTex) $(terminaltablesPdf)

all: $(csv2table) $(placetable) $(terminaltables) $(panfluteCsvTables)
clean:
	rm -f $(csv2table) $(placetable) $(terminaltables) $(panfluteCsvTables)

# csv2table
csv2table/%.source.md: source/%.csv
	mkdir -p csv2table
	printf "%s\n" "~~~{.table inlinemarkdown=yes}" > $@
	cat $< >> $@
	printf "%s\n" "" "~~~" >> $@
csv2table/%.native: csv2table/%.source.md
	pandoc --filter pandoc-csv2table -s -o $@ $< -t native
csv2table/%.target.md: csv2table/%.source.md
	pandoc --filter pandoc-csv2table -s -o $@ $<
csv2table/%.html: csv2table/%.source.md
	pandoc --filter pandoc-csv2table -s -o $@ $<
csv2table/%.tex: csv2table/%.source.md
	pandoc --filter pandoc-csv2table -s -o $@ $<
csv2table/%.pdf: csv2table/%.source.md
	pandoc --filter pandoc-csv2table -s -o $@ $<

# placetable
placetable/%.source.md: source/%.csv
	mkdir -p placetable
	printf "%s\n" "~~~{.table inlinemarkdown=yes}" > $@
	cat $< >> $@
	printf "%s\n" "" "~~~" >> $@
placetable/%.native: placetable/%.source.md
	pandoc --filter pandoc-placetable -s -o $@ $< -t native
placetable/%.target.md: placetable/%.source.md
	pandoc --filter pandoc-placetable -s -o $@ $<
placetable/%.html: placetable/%.source.md
	pandoc --filter pandoc-placetable -s -o $@ $<
placetable/%.tex: placetable/%.source.md
	pandoc --filter pandoc-placetable -s -o $@ $<
placetable/%.pdf: placetable/%.source.md
	pandoc --filter pandoc-placetable -s -o $@ $< || true

# panflute csv-tables
panflute-csv-tables/%.source.md: source/%.csv
	mkdir -p panflute-csv-tables
	printf "%s\n" "~~~csv" "has-header: True" "---" > $@
	cat $< >> $@
	printf "%s\n" "" "~~~" >> $@
panflute-csv-tables/%.native: panflute-csv-tables/%.source.md
	pandoc --filter bin/csv-tables.py -s -o $@ $< -t native
panflute-csv-tables/%.target.md: panflute-csv-tables/%.source.md
	pandoc --filter bin/csv-tables.py -s -o $@ $<
panflute-csv-tables/%.html: panflute-csv-tables/%.source.md
	pandoc --filter bin/csv-tables.py -s -o $@ $<
panflute-csv-tables/%.tex: panflute-csv-tables/%.source.md
	pandoc --filter bin/csv-tables.py -s -o $@ $<
panflute-csv-tables/%.pdf: panflute-csv-tables/%.source.md
	pandoc --filter bin/csv-tables.py -s -o $@ $< || true

# python terminaltables
terminaltables/%.source.md: source/%.csv
	mkdir -p terminaltables
	bin/pandoc_csv2tables.py $< > $@
terminaltables/%.native: terminaltables/%.source.md
	pandoc -s -o $@ $< -t native
terminaltables/%.target.md: terminaltables/%.source.md
	pandoc -s -o $@ $<
terminaltables/%.html: terminaltables/%.source.md
	pandoc -s -o $@ $<
terminaltables/%.tex: terminaltables/%.source.md
	pandoc -s -o $@ $<
terminaltables/%.pdf: terminaltables/%.source.md
	pandoc -s -o $@ $<
