# Generate dictionaries of species and their phases
def generate_species_phase_dicts(species_list):
    """Generate dictionaries of species and their phases."""
    species_phase_dicts = {}

    for species in species_list:
        if species['phases'] is None:
            # Directly add elements without phases
            key = '_'.join(species['english_name'].lower().split())
            species_phase_dicts[key] = {
                'norwegian_name': species['norwegian_name'],
                'english_name': species['english_name'],
                'latin_name': species['latin_name'],
                'phase': None,
                'row_start_idx': species['row_start_idx'],
                'row_end_idx': species['row_end_idx'],
                'col_start_idx': species['col_start_idx'],
                'col_end_idx': species['col_end_idx']
            }
        else:
            # Handle species with phases normally
            start_table_idx = species['row_start_idx']
            for phase in species['phases']:
                key = f'{"_".join(species["english_name"].lower().split())}_{phase}'
                species_phase_dicts[key] = {
                    'norwegian_name': species['norwegian_name'],
                    'english_name': species['english_name'],
                    'latin_name': species['latin_name'],
                    'phase': phase,
                    'row_start_idx': start_table_idx,
                    'row_end_idx': start_table_idx + 1,
                    'col_start_idx': species['col_start_idx'],
                    'col_end_idx': species['col_end_idx'],
                }
                start_table_idx += 1

    return species_phase_dicts

# Define the list of phases
phases = [
    'greenup',
    'greenup_timespan',
    'flowering',
    'start_ripening',
    'flowering_timespan',
    'start_senescence',
    'start_leaffall',
    'end_leaffall'
]

# Define the list of different species and their phases
species_list = [
    {
        'norwegian_name': 'Nummer', # Number
        'english_name': 'Number',
        'latin_name': '',
        'row_start_idx': 0,
        'row_end_idx': 1,
        'col_start_idx': 0,
        'col_end_idx': 2,
        'phases': None
    },
    {
        'norwegian_name': 'Lokasjon', # Location
        'english_name': 'Location',
        'latin_name': '',
        'row_start_idx': 0,
        'row_end_idx': 1,
        'col_start_idx': 2,
        'col_end_idx': 15,
        'phases': None
    },
    {
        'norwegian_name': 'Fylke', # County
        'english_name': 'County',
        'latin_name': '',
        'row_start_idx': 0,
        'row_end_idx': 1,
        'col_start_idx': 15,
        'col_end_idx': 20,
        'phases': None
    },
    {
        'norwegian_name': 'Posisjon', # Position
        'english_name': 'Position',
        'latin_name': '',
        'row_start_idx': 5,
        'row_end_idx': 19,
        'col_start_idx': 0,
        'col_end_idx': 1,
        'phases': None
    },
    {
        'norwegian_name': 'HOH', # HASL
        'english_name': 'HASL',
        'latin_name': '',
        'row_start_idx': 5,
        'row_end_idx': 19,
        'col_start_idx': 0,
        'col_end_idx': 1,
        'phases': None
    },
    {
        'norwegian_name': 'DH', # Distance to sea in kilometers
        'english_name': 'DS',
        'latin_name': '',
        'row_start_idx': 5,
        'row_end_idx': 19,
        'col_start_idx': 0,
        'col_end_idx': 1,
        'phases': None
    },
    {
        'norwegian_name': 'Hestehov',
        'english_name': 'Coltsfoot',
        'latin_name': 'Tussilago farfara',
        'row_start_idx': 2,
        'row_end_idx': 3,
        'col_start_idx': 2,
        'col_end_idx': 3,
        'phases': ['flowering', 'fruit', 'timespan']
    },
    {
        'norwegian_name': 'Blåveis',
        'english_name': 'Liverleaf',
        'latin_name': 'Hepatica nobilis',
        'row_start_idx': 2,
        'row_end_idx': 3,
        'col_start_idx': 3,
        'col_end_idx': 4,
        'phases': ['flowering', 'fruit', 'timespan']
    },
    {
        'norwegian_name': 'Hvitveis',
        'english_name': 'Wood anemone',
        'latin_name': 'Anemone nemorosa',
        'row_start_idx': 2,
        'row_end_idx': 3,
        'col_start_idx': 4,
        'col_end_idx': 5,
        'phases': ['flowering', 'fruit', 'timespan']
    },
    {
        'norwegian_name': 'Rødsildre',
        'english_name': 'Purple saxifrage',
        'latin_name': 'Saxifraga oppositifolia',
        'row_start_idx': 2,
        'row_end_idx': 3,
        'col_start_idx': 5,
        'col_end_idx': 6,
        'phases': ['flowering', 'fruit', 'timespan']
    },
    {
        'norwegian_name': 'Nyresildre',
        'english_name': 'Meadow saxifrage',
        'latin_name': 'Saxifraga nemorosa',
        'row_start_idx': 2,
        'row_end_idx': 3,
        'col_start_idx': 6,
        'col_end_idx': 7,
        'phases': ['flowering', 'fruit', 'timespan']
    },
    {
        'norwegian_name': 'Maria nøklebånd',
        'english_name': 'Cowslip',
        'latin_name': 'Primula veris',
        'row_start_idx': 2,
        'row_end_idx': 3,
        'col_start_idx': 7,
        'col_end_idx': 8,
        'phases': ['flowering', 'fruit', 'timespan']
    },
    {
        'norwegian_name': 'Soleihov',
        'english_name': 'Marsh marigold',
        'latin_name': 'Caltha palustris',
        'row_start_idx': 2,
        'row_end_idx': 3,
        'col_start_idx': 8,
        'col_end_idx': 9,
        'phases': ['flowering', 'fruit', 'timespan']
    },
    {
        'norwegian_name': 'Ballblom',
        'english_name': 'Globeflower',
        'latin_name': 'Trollius europaeus',
        'row_start_idx': 2,
        'row_end_idx': 3,
        'col_start_idx': 9,
        'col_end_idx': 10,
        'phases': ['flowering', 'fruit', 'timespan']
    },
    {
        'norwegian_name': 'Liljekonvall',
        'english_name': 'Lily of the valley',
        'latin_name': 'Convallaria majalis',
        'row_start_idx': 2,
        'row_end_idx': 3,
        'col_start_idx': 10,
        'col_end_idx': 11,
        'phases': ['flowering', 'fruit', 'timespan']
    },
    {
        'norwegian_name': 'Markjordbær',
        'english_name': 'Wild strawberry',
        'latin_name': 'Fragaria vesca',
        'row_start_idx': 2,
        'row_end_idx': 3,
        'col_start_idx': 11,
        'col_end_idx': 12,
        'phases': ['flowering', 'fruit', 'timespan']
    },
    {
        'norwegian_name': 'Gjøksyre',
        'english_name': 'Wood sorrel',
        'latin_name': 'Oxalis acetosella',
        'row_start_idx': 2,
        'row_end_idx': 3,
        'col_start_idx': 12,
        'col_end_idx': 13,
        'phases': ['flowering', 'fruit', 'timespan']
    },
    {
        'norwegian_name': 'Skogstjerne',
        'english_name': 'Arctic starflower',
        'latin_name': 'Trientalis europaea',
        'row_start_idx': 2,
        'row_end_idx': 3,
        'col_start_idx': 13,
        'col_end_idx': 14,
        'phases': ['flowering', 'fruit', 'timespan']
    },
    {
        'norwegian_name': 'Linnea',
        'english_name': 'Linnaea',
        'latin_name': 'Linnaea borealis',
        'row_start_idx': 2,
        'row_end_idx': 3,
        'col_start_idx': 14,
        'col_end_idx': 15,
        'phases': ['flowering', 'fruit', 'timespan']
    },
    {
        'norwegian_name': 'Blåbær',
        'english_name': 'Blueberry',
        'latin_name': 'Vaccinium myrtillus',
        'row_start_idx': 2,
        'row_end_idx': 3,
        'col_start_idx': 15,
        'col_end_idx': 16,
        'phases': ['flowering', 'fruit', 'timespan']
    },
    {
        'norwegian_name': 'Multer',
        'english_name': 'Cloudberry',
        'latin_name': 'Rubus chamaemorus',
        'row_start_idx': 2,
        'row_end_idx': 3,
        'col_start_idx': 16,
        'col_end_idx': 17,
        'phases': ['flowering', 'fruit', 'timespan']
    },
    {
        'norwegian_name': 'Geitrams',
        'english_name': 'Fireweed',
        'latin_name': 'Epilobium angustifolium',
        'row_start_idx': 2,
        'row_end_idx': 3,
        'col_start_idx': 17,
        'col_end_idx': 18,
        'phases': ['flowering', 'fruit', 'timespan']
    },
    {
        'norwegian_name': 'Mjødurt',
        'english_name': 'Meadowsweet',
        'latin_name': 'Spirea ulmaria',
        'row_start_idx': 2,
        'row_end_idx': 3,
        'col_start_idx': 18,
        'col_end_idx': 19,
        'phases': ['flowering', 'fruit', 'timespan']
    },
    {
        'norwegian_name': 'Røsslyng',
        'english_name': 'Heather',
        'latin_name': 'Calluna vulgaris',
        'row_start_idx': 2,
        'row_end_idx': 3,
        'col_start_idx': 19,
        'col_end_idx': 20,
        'phases': ['flowering', 'fruit', 'timespan']
    },
    {
        'norwegian_name': 'Hassel',
        'english_name': 'Hazel',
        'latin_name': 'Corylus avellana',
        'row_start_idx': 10,
        'row_end_idx': 11,
        'col_start_idx': 3,
        'col_end_idx': 4,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening', 'flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Gråor',  # Grey Alder coordinates, species 19
        'english_name': 'Grey Alder',
        'latin_name': 'Alnus incana',
        'row_start_idx': 10,
        'row_end_idx': 11,
        'col_start_idx': 4,
        'col_end_idx': 5,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening', 'flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Selje',  # Goat Willow coordinates, species 20
        'english_name': 'Goat Willow',
        'latin_name': 'Salix caprea',
        'row_start_idx': 10,
        'row_end_idx': 11,
        'col_start_idx': 5,
        'col_end_idx': 6,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening', 'flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Osp',  # Aspen coordinates, species 21
        'english_name': 'Aspen',
        'latin_name': 'Populus tremula',
        'row_start_idx': 10,
        'row_end_idx': 11,
        'col_start_idx': 6,
        'col_end_idx': 7,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening', 'flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Lavlandsbjerk',  # Silver Birch coordinates, species 22
        'english_name': 'Silver Birch',
        'latin_name': 'Betula verrucosa',
        'row_start_idx': 10,
        'row_end_idx': 11,
        'col_start_idx': 7,
        'col_end_idx': 8,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening', 'flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Fjellbjerk',  # Downy Birch coordinates, species 23
        'english_name': 'Downy Birch',
        'latin_name': 'Betula odorata',
        'row_start_idx': 10,
        'row_end_idx': 11,
        'col_start_idx': 8,
        'col_end_idx': 9,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening', 'flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Alm',  # Wych Elm coordinates, species 24
        'english_name': 'Wych Elm',
        'latin_name': 'Ulmus montana',
        'row_start_idx': 10,
        'row_end_idx': 11,
        'col_start_idx': 9,
        'col_end_idx': 10,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening', 'flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Sommerek',  # Pedunculate Oak coordinates, species 25
        'english_name': 'Pedunculate Oak',
        'latin_name': 'Quercus pedunculata',
        'row_start_idx': 10,
        'row_end_idx': 11,
        'col_start_idx': 10,
        'col_end_idx': 11,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening', 'flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Bøk',  # European Beech coordinates, species 26
        'english_name': 'European Beech',
        'latin_name': 'Fagus silvatica',
        'row_start_idx': 10,
        'row_end_idx': 11,
        'col_start_idx': 11,
        'col_end_idx': 12,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening', 'flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Hegg',  # Bird Cherry coordinates, species 27
        'english_name': 'Bird Cherry',
        'latin_name': 'Prunus padus',
        'row_start_idx': 10,
        'row_end_idx': 11,
        'col_start_idx': 12,
        'col_end_idx': 13,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening', 'flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Slåpetorn',  # Blackthorn coordinates, species 28
        'english_name': 'Blackthorn',
        'latin_name': 'Prunus spinosa',
        'row_start_idx': 10,
        'row_end_idx': 11,
        'col_start_idx': 13,
        'col_end_idx': 14,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening', 'flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Kirsebær',  # Cherry coordinates, species 29
        'english_name': 'Cherry',
        'latin_name': 'Pyrus malus',
        'row_start_idx': 10,
        'row_end_idx': 11,
        'col_start_idx': 14,
        'col_end_idx': 15,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening', 'flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Eple',  # Apple coordinates, species 30
        'english_name': 'Apple',
        'latin_name': 'Pyrus malus',
        'row_start_idx': 10,
        'row_end_idx': 11,
        'col_start_idx': 15,
        'col_end_idx': 16,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening', 'flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Rips',  # Redcurrant coordinates, species 31
        'english_name': 'Redcurrant',
        'latin_name': 'Ribes rubrum',
        'row_start_idx': 10,
        'row_end_idx': 11,
        'col_start_idx': 16,
        'col_end_idx': 17,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening', 'flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Stikkelsbær',  # Gooseberry coordinates, species 32
        'english_name': 'Gooseberry',
        'latin_name': 'Ribes grossularia',
        'row_start_idx': 10,
        'row_end_idx': 11,
        'col_start_idx': 17,
        'col_end_idx': 18,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening', 'flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Bringebær',  # Raspberry coordinates, species 33
        'english_name': 'Raspberry',
        'latin_name': 'Rubus idaeus',
        'row_start_idx': 10,
        'row_end_idx': 11,
        'col_start_idx': 18,
        'col_end_idx': 19,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening', 'flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Rogn',  # Rowan coordinates, species 34
        'english_name': 'Rowan',
        'latin_name': 'Sorbus aucuparia',
        'row_start_idx': 10,
        'row_end_idx': 11,
        'col_start_idx': 19,
        'col_end_idx': 20,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening', 'flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Lønn',  # Norway Maple coordinates, species 35
        'english_name': 'Norway Maple',
        'latin_name': 'Acer platanoides',
        'row_start_idx': 19,
        'row_end_idx': 20,
        'col_start_idx': 2,
        'col_end_idx': 3,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening']
    },
    {
        'norwegian_name': 'Lind',  # Small-leaved Lime coordinates, species 36
        'english_name': 'Small leaved Lime',
        'latin_name': 'Tilia cordata',
        'row_start_idx': 19,
        'row_end_idx': 20,
        'col_start_idx': 3,
        'col_end_idx': 4,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening']
    },
    {
        'norwegian_name': 'Syren',  # Common Lilac coordinates, species 37
        'english_name': 'Common Lilac',
        'latin_name': 'Syringa vulgaris',
        'row_start_idx': 19,
        'row_end_idx': 20,
        'col_start_idx': 4,
        'col_end_idx': 5,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening']
    },
    {
        'norwegian_name': 'Ask',  # European Ash coordinates, species 38
        'english_name': 'European Ash',
        'latin_name': 'Fraxinus excelsior',
        'row_start_idx': 19,
        'row_end_idx': 20,
        'col_start_idx': 5,
        'col_end_idx': 6,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening']
    },
    {
        'norwegian_name': 'Nyperose',  # Dog Rose coordinates, species 39
        'english_name': 'Dog Rose',
        'latin_name': 'Rosa sp.',
        'row_start_idx': 19,
        'row_end_idx': 20,
        'col_start_idx': 6,
        'col_end_idx': 7,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening']
    },
    {
        'norwegian_name': 'Jasmin',  # Mock Orange coordinates, species 40
        'english_name': 'Mock Orange',
        'latin_name': 'Philadelphus coronarius',
        'row_start_idx': 19,
        'row_end_idx': 20,
        'col_start_idx': 7,
        'col_end_idx': 8,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening']
    },
    {
        'norwegian_name': 'Gran',  # Norway Spruce coordinates, species 41
        'english_name': 'Norway Spruce',
        'latin_name': 'Picea excelsa',
        'row_start_idx': 19,
        'row_end_idx': 20,
        'col_start_idx': 8,
        'col_end_idx': 9,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening']
    },
    {
        'norwegian_name': 'Furu',
        'english_name': 'Pine',
        'latin_name': 'Pinus sylvestris',
        'row_start_idx': 19,
        'row_end_idx': 20,
        'col_start_idx': 9,
        'col_end_idx': 10,
        'phases': ['greenup', 'greenup_timespan', 'flowering', 'start_ripening']
    },
    {
        'norwegian_name': 'Lønn',  # Norway Maple coordinates, species 35
        'english_name': 'Norway Maple',
        'latin_name': 'Acer platanoides',
        'row_start_idx': 19,
        'row_end_idx': 20,
        'col_start_idx': 12,
        'col_end_idx': 13,
        'phases': ['flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Lind',  # Small-leaved Lime coordinates, species 36
        'english_name': 'Small leaved Lime',
        'latin_name': 'Tilia cordata',
        'row_start_idx': 19,
        'row_end_idx': 20,
        'col_start_idx': 13,
        'col_end_idx': 14,
        'phases': ['flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Syren',  # Common Lilac coordinates, species 37
        'english_name': 'Common Lilac',
        'latin_name': 'Syringa vulgaris',
        'row_start_idx': 19,
        'row_end_idx': 20,
        'col_start_idx': 14,
        'col_end_idx': 15,
        'phases': ['flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Ask',  # European Ash coordinates, species 38
        'english_name': 'European Ash',
        'latin_name': 'Fraxinus excelsior',
        'row_start_idx': 19,
        'row_end_idx': 20,
        'col_start_idx': 15,
        'col_end_idx': 16,
        'phases': ['flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Nyperose',  # Dog Rose coordinates, species 39
        'english_name': 'Dog Rose',
        'latin_name': 'Rosa sp.',
        'row_start_idx': 19,
        'row_end_idx': 20,
        'col_start_idx': 16,
        'col_end_idx': 17,
        'phases': ['flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Jasmin',  # Mock Orange coordinates, species 40
        'english_name': 'Mock Orange',
        'latin_name': 'Philadelphus coronarius',
        'row_start_idx': 19,
        'row_end_idx': 20,
        'col_start_idx': 17,
        'col_end_idx': 18,
        'phases': ['flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Gran',  # Norway Spruce coordinates, species 41
        'english_name': 'Norway Spruce',
        'latin_name': 'Picea excelsa',
        'row_start_idx': 19,
        'row_end_idx': 20,
        'col_start_idx': 18,
        'col_end_idx': 19,
        'phases': ['flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Furu',
        'english_name': 'Pine',
        'latin_name': 'Pinus sylvestris',
        'row_start_idx': 19,
        'row_end_idx': 20,
        'col_start_idx': 19,
        'col_end_idx': 20,
        'phases': ['flowering_timespan', 'start_senescence', 'start_leaffall', 'end_leaffall']
    },
    {
        'norwegian_name': 'Antall observasjonsår',
        'english_name': 'Number of observation years',
        'latin_name': '',
        'row_start_idx': 6,
        'row_end_idx': 7,
        'col_start_idx': 1,
        'col_end_idx': 2,
        'phases': None
    },
    {
        'norwegian_name': 'Løvsprett ved tregrensen',
        'english_name': 'Leafout at the treeline',
        'latin_name': '',
        'row_start_idx': 6,
        'row_end_idx': 7,
        'col_start_idx': 2,
        'col_end_idx': 3,
        'phases': None
    },
    {
        'norwegian_name': 'Gjennomsnittelig høyde hvor løvsprett ved tregrensen måles',
        'english_name': 'Average height where leafout at the treeline is measured',
        'latin_name': '',
        'row_start_idx': 6,
        'row_end_idx': 7,
        'col_start_idx': 3,
        'col_end_idx': 4,
        'phases': None
    },
    {
        'norwegian_name': 'Type tre som definerer tregrensen',
        'english_name': 'Type of tree that defines the treeline',
        'latin_name': '',
        'row_start_idx': 6,
        'row_end_idx': 7,
        'col_start_idx': 4,
        'col_end_idx': 5,
        'phases': None
    },
    {
        'norwegian_name': 'Isløsning',
        'english_name': 'Ice break',
        'latin_name': '',
        'row_start_idx': 6,
        'row_end_idx': 7,
        'col_start_idx': 5,
        'col_end_idx': 6,
        'phases': None
    },
    {
        'norwegian_name': 'Elver eller innsjøer definerer isløsning', # e -> river, s -> lake
        'english_name': 'Rivers or lakes define the ice break',
        'latin_name': '',
        'row_start_idx': 6,
        'row_end_idx': 7,
        'col_start_idx': 6,
        'col_end_idx': 7,
        'phases': None
    },
    {
        'norwegian_name': 'Tid mellom isløsning elver og vann',
        'english_name': 'Time between ice break rivers and lakes',
        'latin_name': '',
        'row_start_idx': 6,
        'row_end_idx': 7,
        'col_start_idx': 7,
        'col_end_idx': 8,
        'phases': None
    },
    {
        'norwegian_name': 'Ingen is prosent åpent vann hele året',
        'english_name': 'No ice percentage open water all year',
        'latin_name': '',
        'row_start_idx': 6,
        'row_end_idx': 7,
        'col_start_idx': 8,
        'col_end_idx': 9,
        'phases': None
    },
    {
        'norwegian_name': 'Teleløsning',
        'english_name': 'No permafrost',
        'latin_name': '',
        'row_start_idx': 6,
        'row_end_idx': 7,
        'col_start_idx': 9,
        'col_end_idx': 10,
        'phases': None
    },
    {
        'norwegian_name': 'Prosent telefritt hele året',
        'english_name': 'Percentage without permafrost all year',
        'latin_name': '',
        'row_start_idx': 6,
        'row_end_idx': 7,
        'col_start_idx': 10,
        'col_end_idx': 11,
        'phases': None
    },
    {
        'norwegian_name': 'Første pløyedag',
        'english_name': 'First ploughing day',
        'latin_name': '',
        'row_start_idx': 6,
        'row_end_idx': 7,
        'col_start_idx': 11,
        'col_end_idx': 12,
        'phases': None
    },
    {
        'norwegian_name': 'Første spiring åker',
        'english_name': 'First greenup fields',
        'latin_name': '',
        'row_start_idx': 6,
        'row_end_idx': 7,
        'col_start_idx': 12,
        'col_end_idx': 13,
        'phases': None
    },
    {
        'norwegian_name': 'Feslepp',
        'english_name': 'Release of cattle',
        'latin_name': '',
        'row_start_idx': 6,
        'row_end_idx': 7,
        'col_start_idx': 13,
        'col_end_idx': 14,
        'phases': None
    },
    {
        'norwegian_name': 'Sau eller ku definerer feslepp',
        'english_name': 'Sheep or cattle define release of cattle',
        'latin_name': '',
        'row_start_idx': 6,
        'row_end_idx': 7,
        'col_start_idx': 14,
        'col_end_idx': 15,
        'phases': None
    },
    {
        'norwegian_name': 'Tid mellom feslepp sau og ku',
        'english_name': 'Time between sheep and cattle release',
        'latin_name': '',
        'row_start_idx': 6,
        'row_end_idx': 7,
        'col_start_idx': 15,
        'col_end_idx': 16,
        'phases': None
    },
    {
        'norwegian_name': 'Såtid bygg',
        'english_name': 'Sowtime barley',
        'latin_name': '',
        'row_start_idx': 6,
        'row_end_idx': 7,
        'col_start_idx': 16,
        'col_end_idx': 17,
        'phases': None
    },
    {
        'norwegian_name': 'Såtid havre',
        'english_name': 'Sowtime oats',
        'latin_name': '',
        'row_start_idx': 6,
        'row_end_idx': 7,
        'col_start_idx': 17,
        'col_end_idx': 18,
        'phases': None
    },
    {
        'norwegian_name': 'Såtid hvete',
        'english_name': 'Sowtime wheat',
        'latin_name': '',
        'row_start_idx': 6,
        'row_end_idx': 7,
        'col_start_idx': 18,
        'col_end_idx': 19,
        'phases': None
    },
    {
        'norwegian_name': 'Settetid poteter',
        'english_name': 'Potato planting',
        'latin_name': '',
        'row_start_idx': 6,
        'row_end_idx': 7,
        'col_start_idx': 18,
        'col_end_idx': 19,
        'phases': None
    },
    {
        'norwegian_name': 'Første observasjon stær',
        'english_name': 'First observation of starling',
        'latin_name': '',
        'row_start_idx': 8,
        'row_end_idx': 9,
        'col_start_idx': 1,
        'col_end_idx': 2,
        'phases': None
    },
    {
        'norwegian_name': 'Prosent stær overvintret',
        'english_name': 'Percentage of starling overwintering',
        'latin_name': '',
        'row_start_idx': 8,
        'row_end_idx': 9,
        'col_start_idx': 2,
        'col_end_idx': 3,
        'phases': None
    },
    {
        'norwegian_name': 'Første observasjon lerke',
        'english_name': 'First observation of lark',
        'latin_name': '',
        'row_start_idx': 8,
        'row_end_idx': 9,
        'col_start_idx': 3,
        'col_end_idx': 4,
        'phases': None
    },
    {
        'norwegian_name': 'Første observasjon måltrost',
        'english_name': 'First observation of song thrush',
        'latin_name': '',
        'row_start_idx': 8,
        'row_end_idx': 9,
        'col_start_idx': 4,
        'col_end_idx': 5,
        'phases': None
    },
    {
        'norwegian_name': 'Første observasjon linerle',
        'english_name': 'First observation of wagtail',
        'latin_name': '',
        'row_start_idx': 8,
        'row_end_idx': 9,
        'col_start_idx': 5,
        'col_end_idx': 6,
        'phases': None
    },
    {
        'norwegian_name': 'Første observasjon svale',
        'english_name': 'First observation of swallow',
        'latin_name': '',
        'row_start_idx': 8,
        'row_end_idx': 9,
        'col_start_idx': 6,
        'col_end_idx': 7,
        'phases': None
    },
    {
        'norwegian_name': 'Første observasjon gjøk',
        'english_name': 'First observation of cuckoo',
        'latin_name': '',
        'row_start_idx': 8,
        'row_end_idx': 9,
        'col_start_idx': 7,
        'col_end_idx': 8,
        'phases': None
    },
    {
        'norwegian_name': 'Åker moden for slått',
        'english_name': 'Field ripe for harvesting',
        'latin_name': '',
        'row_start_idx': 8,
        'row_end_idx': 9,
        'col_start_idx': 8,
        'col_end_idx': 9,
        'phases': None
    },
    {
        'norwegian_name': 'Vinterrug moden for slått',
        'english_name': 'Winter rye ripe for harvesting',
        'latin_name': '',
        'row_start_idx': 8,
        'row_end_idx': 9,
        'col_start_idx': 9,
        'col_end_idx': 10,
        'phases': None
    },
    {
        'norwegian_name': 'Prosent umodnet vinterrug',
        'english_name': 'Percentage of unripe winter rye',
        'latin_name': '',
        'row_start_idx': 8,
        'row_end_idx': 9,
        'col_start_idx': 10,
        'col_end_idx': 11,
        'phases': None
    },
    {
        'norwegian_name': 'Havre moden for slått',
        'english_name': 'Oats ripe for harvesting',
        'latin_name': '',
        'row_start_idx': 8,
        'row_end_idx': 9,
        'col_start_idx': 11,
        'col_end_idx': 12,
        'phases': None
    },
    {
        'norwegian_name': 'Havre modningstid',
        'english_name': 'Oats maturing time',
        'latin_name': '',
        'row_start_idx': 8,
        'row_end_idx': 9,
        'col_start_idx': 12,
        'col_end_idx': 13,
        'phases': None
    },
    {
        'norwegian_name': 'Prosent umodnet havre',
        'english_name': 'Percentage of unripe barley',
        'latin_name': '',
        'row_start_idx': 8,
        'row_end_idx': 9,
        'col_start_idx': 13,
        'col_end_idx': 14,
        'phases': None
    },
    {
        'norwegian_name': 'Bygg moden for slått',
        'english_name': 'Barley ripe for harvesting',
        'latin_name': '',
        'row_start_idx': 8,
        'row_end_idx': 9,
        'col_start_idx': 14,
        'col_end_idx': 15,
        'phases': None
    },
    {
        'norwegian_name': 'Bygg modningstid',
        'english_name': 'Barley maturing time',
        'latin_name': '',
        'row_start_idx': 8,
        'row_end_idx': 9,
        'col_start_idx': 15,
        'col_end_idx': 16,
        'phases': None
    },
    {
        'norwegian_name': 'Prosent umodnet bygg',
        'english_name': 'Percentage of unripe barley',
        'latin_name': '',
        'row_start_idx': 8,
        'row_end_idx': 9,
        'col_start_idx': 16,
        'col_end_idx': 17,
        'phases': None
    },
    {
        'norwegian_name': 'Hvete moden for slått',
        'english_name': 'Wheat ripe for harvesting',
        'latin_name': '',
        'row_start_idx': 8,
        'row_end_idx': 9,
        'col_start_idx': 17,
        'col_end_idx': 18,
        'phases': None
    },
    {
        'norwegian_name': 'Hvete modningstid',
        'english_name': 'Wheat maturing time',
        'latin_name': '',
        'row_start_idx': 8,
        'row_end_idx': 9,
        'col_start_idx': 18,
        'col_end_idx': 19,
        'phases': None
    },
    {
        'norwegian_name': 'Prosent umodnet hvete',
        'english_name': 'Percentage of unripe wheat',
        'latin_name': '',
        'row_start_idx': 8,
        'row_end_idx': 9,
        'col_start_idx': 19,
        'col_end_idx': 20,
        'phases': None
    }
] 