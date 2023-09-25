const dealerships = [
    {
      "id": 1,
      "city": "El Paso",
      "state": "Texas",
      "st": "TX",
      "address": "3 Nova Court",
      "zip": "88563",
      "lat": 31.6948,
      "long": -106.3,
      "short_name": "Holdlamis",
      "full_name": "Holdlamis Car Dealership"
    },
    {
      "id": 2,
      "city": "Minneapolis",
      "state": "Minnesota",
      "st": "MN",
      "address": "6337 Butternut Crossing",
      "zip": "55402",
      "lat": 44.9762,
      "long": -93.2759,
      "short_name": "Temp",
      "full_name": "Temp Car Dealership"
    }
  ];
  
  // Print the id property of each object
  for (const dealership of dealerships) {
    console.log(dealership.id);
    console.log(dealership.address);
    console.log(dealership.zip);
    console.log(dealership.city);
    console.log(dealership.full_name);
    console.log('--------------')
  }