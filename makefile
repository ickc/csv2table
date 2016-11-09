csvSource := $(wildcard source/*.csv)
mdSource := $(patsubst %.csv,%.md,$(csvSource))

# csv2table
csv2tableNative := $(patsubst source/%.csv,csv2table/%.native,$(csvSource))
csv2tableMd := $(patsubst source/%.csv,csv2table/%.md,$(csvSource))
csv2tableHtml := $(patsubst source/%.csv,csv2table/%.html,$(csvSource))
csv2tableTex := $(patsubst source/%.csv,csv2table/%.tex,$(csvSource))
csv2tablePdf := $(patsubst source/%.csv,csv2table/%.pdf,$(csvSource))
# placetable
placetableNative := $(patsubst source/%.csv,placetable/%.native,$(csvSource))
placetableMd := $(patsubst source/%.csv,placetable/%.md,$(csvSource))
placetableHtml := $(patsubst source/%.csv,placetable/%.html,$(csvSource))
placetableTex := $(patsubst source/%.csv,placetable/%.tex,$(csvSource))
placetablePdf := $(patsubst source/%.csv,placetable/%.pdf,$(csvSource))

all: $(mdSource) $(csv2tableNative) $(csv2tableMd) $(csv2tableHtml) $(csv2tableTex) $(csv2tablePdf) $(placetableNative) $(placetableMd) $(placetableHtml) $(placetableTex) $(placetablePdf)
clean:
	rm -f $(mdSource) $(csv2tableNative) $(csv2tableMd) $(csv2tableHtml) $(csv2tableTex) $(csv2tablePdf) $(placetableNative) $(placetableMd) $(placetableHtml) $(placetableTex) $(placetablePdf)

source/%.md: source/%.csv
	printf "%s\n" "~~~{.table inlinemarkdown=yes}" > $@
	cat $< >> $@
	printf "%s\n" "" "~~~" >> $@

csv2table/%.native: source/%.md
	mkdir -p csv2table
	pandoc --filter pandoc-csv2table -s -o $@ $< -t native
csv2table/%.md: source/%.md
	mkdir -p csv2table
	pandoc --filter pandoc-csv2table -s -o $@ $<
csv2table/%.html: source/%.md
	mkdir -p csv2table
	pandoc --filter pandoc-csv2table -s -o $@ $<
csv2table/%.tex: source/%.md
	mkdir -p csv2table
	pandoc --filter pandoc-csv2table -s -o $@ $<
csv2table/%.pdf: source/%.md
	mkdir -p csv2table
	pandoc --filter pandoc-csv2table -s -o $@ $<

placetable/%.native: source/%.md
	mkdir -p placetable
	pandoc --filter pandoc-placetable -s -o $@ $< -t native
placetable/%.md: source/%.md
	mkdir -p placetable
	pandoc --filter pandoc-placetable -s -o $@ $<
placetable/%.html: source/%.md
	mkdir -p placetable
	pandoc --filter pandoc-placetable -s -o $@ $<
placetable/%.tex: source/%.md
	mkdir -p placetable
	pandoc --filter pandoc-placetable -s -o $@ $<
placetable/%.pdf: source/%.md
	mkdir -p placetable
	pandoc --filter pandoc-placetable -s -o $@ $<
