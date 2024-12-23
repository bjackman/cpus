# EVERY CPU EVER IN A PERFECT BEAUTIFUL DATABASE

This was my brief attempt to scrape something useful out of the crappy .csv
files that Intel and AMD provide on their websites and then join them against a
table of which models have which microarchitecture.

Don't worry we did not forget any CPUs, we got both kinds here.

I think this would basically work, just needs a few hours of grind to get more
data and clean up what we have.

Expand the gigantic hidden code blocks to see the .csv and a link to where I got them from.

Known issues:

- The Intel CSV is incomplete. Their website doesn't actually seem designed to
  offer this info, its "product comparison" page lets you compare between
  different product lines, and you can in theory compare arbitrarily many SKUs
  with enough clicking around but when you try to actually generate the
  comparison it easily times out if there are more than about 100.

  So I've done that for a bunch of them but there are still way more Intel CPUs
  that haven't been done.\

- [Fixed? Can't remember] Pandas didn't parse the AMD CSV properly so there are
  garbage rows & garbage columns. Sheets parsed it fine So I think this is just
  a job of finding the right `read_csv` args.

- I didn't get a list of Intel uarches, presumably we can do the same as for
  AMD: paste a list of product families into Gemini and say "print a Python dict
  mapping these to the microarchitecture" then double check all the important
  ones. For AMD, Gemini was wrong about the overall Zen version once, and wholly
  hallucinating about 5 vs 5c. Then again, given the need to manually check the
  ones you actually care about, maybe it's better to just do this manually.