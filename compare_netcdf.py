#!/usr/bin/env python3

def main(file1, file2):
    import numpy

    # open datasets
    from xarray import open_dataset
    ds = [open_dataset(f, decode_times=False) for f in (file1, file2)]

    # loop over dimensions and check for differences
    for dname in ds[0].dims:
        if ds[1].dims[dname] != ds[0].dims[dname]:
            print('Dimension %s differs')

    # loop over variables and check for differences
    for vname in ds[0].variables.keys():
       try:
            # Calculate absolute difference
            difference = abs(ds[1].variables[vname].values - ds[0].variables[vname].values)

            # Calculate fractional difference
            average = abs(ds[1].variables[vname].values + ds[0].variables[vname].values) / 2
            if numpy.any((difference > 0) & (average > 0)):
                fractional_difference = numpy.where(
                    (average > 0) & (difference > 0), difference / average, 0
                )
            else:
                fractional_difference = numpy.zeros(1)

            # Report differences
            if abs(difference).max() > 0:
                print(
                    'Variable %s differs (max difference: %e; %f%%)'%(
                        vname, abs(difference).max(), 100.0 * fractional_difference.max()
                    )
                )
       except:
           print('Processing for variable %s failed.'%vname)

    # close datasets
    for d in ds: d.close()


if __name__ == '__main__':
    import plac
    plac.call(main)
