db.getCollection('ekb').find({
   $and:[
      {
         "parameters.flat.0.description":"Коммерческая недвижимость"
      },
      {
         "parameters.flat.description":{
            $ne:"Офисное помещение"
         }
      },
      {
         "location":{
            $exists:true
         },
         "location":{
            $near:{
               $geometry:{
                  type:"Point",
                  coordinates:[
                     60.571037,
                     56.832265
                  ]
               },
               $maxDistance:1000
            }
         }
      }
   ]
})