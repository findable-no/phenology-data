# Start by defining the cell coordinates
# Row coordinates for th eupper tables
row_0 = 0
row_1 = 85
row_2 = 130
row_3 = 180
row_4 = 228
row_5 = 270
row_6 = 320
row_7 = 365
row_8 = 413
row_9 = 455
row_10 = 503
row_11 = 550
row_12 = 595
row_13 = 640
row_14 = 690
row_15 = 735
row_16 = 784
row_17 = 830
row_18 = 871
row_19 = 924
row_20 = 972
row_21 = 1017
row_22 = 1064
row_23 = 1110

# Row coordinates for the lower tables
row_24 = 1187
row_25 = 1281 
row_26 = 1329
row_27 = 1377
row_28 = 1423
row_29 = 1467
row_30 = 1516
row_31 = 1560
row_32 = 1609
row_33 = 1655
row_34 = 1701
row_35 = 1750
row_36 = 1797
row_37 = 1843
row_38 = 1889
row_39 = 1937
row_40 = 1987
row_41 = 2032
row_42 = 2072
row_43 = 2125
row_44 = 2169
row_45 = 2219
row_46 = 2269
row_47 = 2315

# Column coordinates for all tables
col_0 = 0
col_1 = 95
col_2 = 173
col_3 = 257
col_4 = 340
col_5 = 420
col_6 = 504
col_7 = 581
col_8 = 662
col_9 = 747
col_10 = 825
col_11 = 905
col_12 = 988
col_13 = 1070
col_14 = 1150
col_15 = 1232
col_16 = 1312
col_17 = 1398
col_18 = 1475
col_19 = 1549
col_20 = 1630

# Define the location of the different observations

# Number coordinates
number_cell = {'norwegian_name': 'Nummer',
               'english_name': 'Number',
               'latin_name': '',
               'upper_table_row_start': row_0,
               'upper_table_row_end': row_1,
               'lower_table_row_start': row_24,
               'lower_table_row_end': row_25,
               'col_start': col_0,
               'col_end': col_2}

# Location coordinates
location_cell = {'norwegian_name': 'Lokasjon',
                 'english_name': 'Location',
                 'latin_name': '',
                 'upper_table_row_start': row_0,
                 'upper_table_row_end': row_1,
                 'lower_table_row_start': row_24,
                 'lower_table_row_end': row_25,
                 'col_start': col_2,
                 'col_end': col_15}

# County coordinates
county_cell = {'norwegian_name': 'Fylke',
               'english_name': 'County',
               'latin_name': '',
               'upper_table_row_start': row_0,
               'upper_table_row_end': row_1,
               'lower_table_row_start': row_24,
               'lower_table_row_end': row_25,
               'col_start': col_15,
               'col_end': col_20}

# Postion coordinates
position_cell = {'norwegian_name': 'Posisjon',
                 'english_name': 'Position',
                 'latin_name': '',
                 'upper_table_row_start': row_5,
                 'upper_table_row_end': row_19,
                 'lower_table_row_start': row_29,
                 'lower_table_row_end': row_43,
                 'col_start': col_0,
                 'col_end': col_1}

hasl_cell = {'norwegian_name': 'HOH',
             'english_name': 'HASL',
             'latin_name': '',
             'upper_table_row_start': row_5,
             'upper_table_row_end': row_19,
             'lower_table_row_start': row_29,
             'lower_table_row_end': row_43,
             'col_start': col_0,
             'col_end': col_1}

ds_cell = {'norwegian_name': 'DH',
           'english_name': 'DS',
           'latin_name': '',
           'upper_table_row_start': row_5,
           'upper_table_row_end': row_19,
           'lower_table_row_start': row_29,
           'lower_table_row_end': row_43,
           'col_start': col_0,
           'col_end': col_1}

meta_features = [number_cell, location_cell, county_cell, position_cell, hasl_cell, ds_cell]

# Plant species coordinates

# Coltsfoot
hestehov_flowering_cell = {'norwegian_name': 'Hestehov',
                           'english_name': 'Coltsfoot',
                           'latin_name': 'Tussilago farfara',
                           'phase': 'flowering',
                           'upper_table_row_start': row_2,
                           'upper_table_row_end': row_3,
                           'lower_table_row_start': row_26,
                           'lower_table_row_end': row_27,
                           'col_start': col_2,
                           'col_end': col_3}

hestehov_fruit_cell = {'norwegian_name': 'Hestehov',
                       'english_name': 'Coltsfoot',
                       'latin_name': 'Tussilago farfara',
                       'phase': 'fruit',
                       'upper_table_row_start': row_3,
                       'upper_table_row_end': row_4,
                       'lower_table_row_start': row_27,
                       'lower_table_row_end': row_28,
                       'col_start': col_2,
                       'col_end': col_3}

hestehov_timespan_cell = {'norwegian_name': 'Hestehov',
                         'english_name': 'Coltsfoot',
                         'latin_name': 'Tussilago farfara',
                         'phase': 'timespan',
                         'upper_table_row_start': row_4,
                         'upper_table_row_end': row_5,
                         'lower_table_row_start': row_28,
                         'lower_table_row_end': row_29,
                         'col_start': col_2,
                         'col_end': col_3}

# Liverleaf
liverleaf_flowering_cell = {'norwegian_name': 'Blåveis',
                           'english_name': 'Liverleaf',
                           'latin_name': 'Hepatica nobilis',
                           'phase': 'flowering',
                           'upper_table_row_start': row_2,
                           'upper_table_row_end': row_3,
                           'lower_table_row_start': row_26,
                           'lower_table_row_end': row_27,
                           'col_start': col_3,
                           'col_end': col_4}

liverleaf_fruit_cell = {'norwegian_name': 'Blåveis',
                       'english_name': 'Liverleaf',
                       'latin_name': 'Hepatica nobilis',
                       'phase': 'fruit',
                       'upper_table_row_start': row_3,
                       'upper_table_row_end': row_4,
                       'lower_table_row_start': row_27,
                       'lower_table_row_end': row_28,
                       'col_start': col_3,
                       'col_end': col_4}

liverleaf_timespan_cell = {'norwegian_name': 'Blåveis',
                          'english_name': 'Liverleaf',
                          'latin_name': 'Hepatica nobilis',
                          'phase': 'timespan',
                          'upper_table_row_start': row_4,
                          'upper_table_row_end': row_5,
                          'lower_table_row_start': row_28,
                          'lower_table_row_end': row_29,
                          'col_start': col_3,
                          'col_end': col_4}

# Wood anemone
wood_anemone_flowering_cell = {'norwegian_name': 'Hvitveis',
                               'english_name': 'Wood anemone',
                               'latin_name': 'Anemone nemorosa',
                               'phase': 'flowering',
                               'upper_table_row_start': row_2,
                               'upper_table_row_end': row_3,
                               'lower_table_row_start': row_26,
                               'lower_table_row_end': row_27,
                               'col_start': col_4,
                               'col_end': col_5}

wood_anemone_fruit_cell = {'norwegian_name': 'Hvitveis',
                           'english_name': 'Wood anemone',
                           'latin_name': 'Anemone nemorosa',
                           'phase': 'fruit',
                           'upper_table_row_start': row_3,
                           'upper_table_row_end': row_4,
                           'lower_table_row_start': row_27,
                           'lower_table_row_end': row_28,
                           'col_start': col_4,
                           'col_end': col_5}

wood_anemone_timespan_cell = {'norwegian_name': 'Hvitveis',
                              'english_name': 'Wood anemone',
                              'latin_name': 'Anemone nemorosa',
                              'phase': 'timespan',
                              'upper_table_row_start': row_4,
                              'upper_table_row_end': row_5,
                              'lower_table_row_start': row_28,
                              'lower_table_row_end': row_29,
                              'col_start': col_4,
                              'col_end': col_5}

# Purple saxifrage
purple_saxifrage_flowering_cell = {'norwegian_name': 'Rødsildre',
                                  'english_name': 'Purple saxifrage',
                                  'latin_name': 'Saxifraga oppositifolia',
                                  'phase': 'flowering',
                                  'upper_table_row_start': row_2,
                                  'upper_table_row_end': row_3,
                                  'lower_table_row_start': row_26,
                                  'lower_table_row_end': row_27,
                                  'col_start': col_5,
                                  'col_end': col_6}

purple_saxifrage_fruit_cell = {'norwegian_name': 'Rødsildre',
                              'english_name': 'Purple saxifrage',
                              'latin_name': 'Saxifraga oppositifolia',
                              'phase': 'fruit',
                              'upper_table_row_start': row_3,
                              'upper_table_row_end': row_4,
                              'lower_table_row_start': row_27,
                              'lower_table_row_end': row_28,
                              'col_start': col_5,
                              'col_end': col_6}

purple_saxifrage_timespan_cell = {'norwegian_name': 'Rødsildre',
                                 'english_name': 'Purple saxifrage',
                                 'latin_name': 'Saxifraga oppositifolia',
                                 'phase': 'timespan',
                                 'upper_table_row_start': row_4,
                                 'upper_table_row_end': row_5,
                                 'lower_table_row_start': row_28,
                                 'lower_table_row_end': row_29,
                                 'col_start': col_5,
                                 'col_end': col_6}

# Meadow saxifrage
meadow_saxifrage_flowering_cell = {'norwegian_name': 'Nyresildre',
                                  'english_name': 'Meadow saxifrage',
                                  'latin_name': 'Saxifraga nemorosa',
                                  'phase': 'flowering',
                                  'upper_table_row_start': row_2,
                                  'upper_table_row_end': row_3,
                                  'lower_table_row_start': row_26,
                                  'lower_table_row_end': row_27,
                                  'col_start': col_6,
                                  'col_end': col_7}

meadow_saxifrage_fruit_cell = {'norwegian_name': 'Nyresildre',
                              'english_name': 'Meadow saxifrage',
                              'latin_name': 'Saxifraga nemorosa',
                              'phase': 'fruit',
                              'upper_table_row_start': row_3,
                              'upper_table_row_end': row_4,
                              'lower_table_row_start': row_27,
                              'lower_table_row_end': row_28,
                              'col_start': col_6,
                              'col_end': col_7}

meadow_saxifrage_timespan_cell = {'norwegian_name': 'Nyresildre',
                                  'english_name': 'Meadow saxifrage',
                                  'latin_name': 'Saxifraga nemorosa',
                                  'phase': 'timespan',
                                  'upper_table_row_start': row_4,
                                  'upper_table_row_end': row_5,
                                  'lower_table_row_start': row_28,
                                  'lower_table_row_end': row_29,
                                  'col_start': col_6,
                                  'col_end': col_7}

# Cowslip
cowslip_flowering_cell = {'norwegian_name': 'Maria nøklebånd',
                          'english_name': 'Cowslip',
                          'latin_name': 'Primula veris',
                          'phase': 'flowering',
                          'upper_table_row_start': row_2,
                          'upper_table_row_end': row_3,
                          'lower_table_row_start': row_26,
                          'lower_table_row_end': row_27,
                          'col_start': col_7,
                          'col_end': col_8}

cowslip_fruit_cell = {'norwegian_name': 'Maria nøklebånd',
                      'english_name': 'Cowslip',
                      'latin_name': 'Primula veris',
                      'phase': 'fruit',
                      'upper_table_row_start': row_3,
                      'upper_table_row_end': row_4,
                      'lower_table_row_start': row_27,
                      'lower_table_row_end': row_28,
                      'col_start': col_7,
                      'col_end': col_8}

cowslip_timespan_cell = {'norwegian_name': 'Maria nøklebånd',
                        'english_name': 'Cowslip',
                        'latin_name': 'Primula veris',
                        'phase': 'timespan',
                        'upper_table_row_start': row_4,
                        'upper_table_row_end': row_5,
                        'lower_table_row_start': row_28,
                        'lower_table_row_end': row_29,
                        'col_start': col_7,
                        'col_end': col_8}

# Marsh marigold
marsh_marigold_flowering_cell = {'norwegian_name': 'Soleihov',
                                'english_name': 'Marsh marigold',
                                'latin_name': 'Caltha palustris',
                                'phase': 'flowering',
                                'upper_table_row_start': row_2,
                                'upper_table_row_end': row_3,
                                'lower_table_row_start': row_26,
                                'lower_table_row_end': row_27,
                                'col_start': col_8,
                                'col_end': col_9}

marsh_marigold_fruit_cell = {'norwegian_name': 'Soleihov',
                            'english_name': 'Marsh marigold',
                            'latin_name': 'Caltha palustris',
                            'phase': 'fruit',
                            'upper_table_row_start': row_3,
                            'upper_table_row_end': row_4,
                            'lower_table_row_start': row_27,
                            'lower_table_row_end': row_28,
                            'col_start': col_8,
                            'col_end': col_9}

marsh_marigold_timespan_cell = {'norwegian_name': 'Soleihov',
                               'english_name': 'Marsh marigold',
                               'latin_name': 'Caltha palustris',
                               'phase': 'timespan',
                               'upper_table_row_start': row_4,
                               'upper_table_row_end': row_5,
                               'lower_table_row_start': row_28,
                               'lower_table_row_end': row_29,
                               'col_start': col_8,
                               'col_end': col_9}

# Globeflower
globeflower_flowering_cell = {'norwegian_name': 'Ballblom',
                             'english_name': 'Globeflower',
                             'latin_name': 'Trollius europaeus',
                             'phase': 'flowering',
                             'upper_table_row_start': row_2,
                             'upper_table_row_end': row_3,
                             'lower_table_row_start': row_26,
                             'lower_table_row_end': row_27,
                             'col_start': col_9,
                             'col_end': col_10}

globeflower_fruit_cell = {'norwegian_name': 'Ballblom',
                         'english_name': 'Globeflower',
                         'latin_name': 'Trollius europaeus',
                         'phase': 'fruit',
                         'upper_table_row_start': row_3,
                         'upper_table_row_end': row_4,
                         'lower_table_row_start': row_27,
                         'lower_table_row_end': row_28,
                         'col_start': col_9,
                         'col_end': col_10}

globeflower_timespan_cell = {'norwegian_name': 'Ballblom',
                            'english_name': 'Globeflower',
                            'latin_name': 'Trollius europaeus',
                            'phase': 'timespan',
                            'upper_table_row_start': row_4,
                            'upper_table_row_end': row_5,
                            'lower_table_row_start': row_28,
                            'lower_table_row_end': row_29,
                            'col_start': col_9,
                            'col_end': col_10}

# Lily of the valley
lily_of_the_valley_flowering_cell = {'norwegian_name': 'Liljeblom',
                                    'english_name': 'Lily of the valley',
                                    'latin_name': 'Convallaria majalis',
                                    'phase': 'flowering',
                                    'upper_table_row_start': row_2,
                                    'upper_table_row_end': row_3,
                                    'lower_table_row_start': row_26,
                                    'lower_table_row_end': row_27,
                                    'col_start': col_10,
                                    'col_end': col_11}

lily_of_the_valley_fruit_cell = {'norwegian_name': 'Liljeblom',
                                'english_name': 'Lily of the valley',
                                'latin_name': 'Convallaria majalis',
                                'phase': 'fruit',
                                'upper_table_row_start': row_3,
                                'upper_table_row_end': row_4,
                                'lower_table_row_start': row_27,
                                'lower_table_row_end': row_28,
                                'col_start': col_10,
                                'col_end': col_11}

lily_of_the_valley_timespan_cell = {'norwegian_name': 'Liljeblom',
                                   'english_name': 'Lily of the valley',
                                   'latin_name': 'Convallaria majalis',
                                   'phase': 'timespan',
                                   'upper_table_row_start': row_4,
                                   'upper_table_row_end': row_5,
                                   'lower_table_row_start': row_28,
                                   'lower_table_row_end': row_29,
                                   'col_start': col_10,
                                   'col_end': col_11}

                         

# Aggregate all plant features
plant_features = [hestehov_flowering_cell,
                  hestehov_fruit_cell,
                  hestehov_timespan_cell,
                  liverleaf_flowering_cell,
                  liverleaf_fruit_cell,
                  liverleaf_timespan_cell,
                  wood_anemone_flowering_cell,
                  wood_anemone_fruit_cell,
                  wood_anemone_timespan_cell,
                  purple_saxifrage_flowering_cell,
                  purple_saxifrage_fruit_cell,
                  purple_saxifrage_timespan_cell,
                  meadow_saxifrage_flowering_cell,
                  meadow_saxifrage_fruit_cell,
                  meadow_saxifrage_timespan_cell,
                  cowslip_flowering_cell,
                  cowslip_fruit_cell,
                  cowslip_timespan_cell,
                  marsh_marigold_flowering_cell,
                  marsh_marigold_fruit_cell,
                  marsh_marigold_timespan_cell,
                  globeflower_flowering_cell,
                  globeflower_fruit_cell,
                  globeflower_timespan_cell,
                  lily_of_the_valley_flowering_cell,
                  lily_of_the_valley_fruit_cell,
                  lily_of_the_valley_timespan_cell]

