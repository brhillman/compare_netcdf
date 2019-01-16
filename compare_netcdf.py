#!/usr/bin/env python3

def main(file1, file2):
    import numpy
    from termcolor import colored

    # open datasets
    from xarray import open_dataset
    ds = [open_dataset(f, decode_times=False) for f in (file1, file2)]

    # loop over dimensions and check for differences
    number_dimension_diffs = 0
    number_dimensions = 0
    for dname in ds[0].dims:
        if dname in ds[1].dims:
            number_dimensions += 1
            if ds[1].dims[dname] != ds[0].dims[dname]:
                print(colored('Dimension %s differs', 'red'))
                number_dimension_diffs += 1
        else:
            print('Warning: %s is not present in both datasets.'%dname)

    # loop over variables and check for differences
    number_variables = 0
    number_variable_diffs = 0
    for vname in ds[0].variables.keys():
        if vname in ds[1].variables.keys():
            number_variables += 1
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
                    print(colored(
                        'Variable %s differs (max difference: %e; %f%%)'%(
                            vname, abs(difference).max(), 100.0 * fractional_difference.max()
                        ), 'red'
                    ))
                    number_variable_diffs += 1
            except:
                print('Processing for variable %s failed.'%vname)
        else:
            print('Warning: variable %s not present in both datasets.'%vname)

    # close datasets
    for d in ds: d.close()

    # Report summaries
    print('Found differences in %i out of %i processed dimensions.'%(number_dimension_diffs, number_dimensions))
    print('Found differences in %i out of %i processed variables.'%(number_variable_diffs, number_variables))

    if number_dimension_diffs == 0 and number_variable_diffs == 0:
        result = colored('PASS', 'green')
    else:
        result = colored('FAIL', 'red')
    print('Result: ', result)


if __name__ == '__main__':
    import plac
    plac.call(main)
