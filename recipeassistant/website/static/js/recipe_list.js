// Recipe List Script

$(document).ready(function(){
    var json_data;
    // var recipes_ARRAY = [];
    // var imageURL_DICT = {};
    // var ingredients_DICT = {};
    // var directions_DICT = {};

    $.ajax({
        dataType: "json",
        url: 'https://0s2cp85xw1.execute-api.us-east-1.amazonaws.com/prod/RecipeUpdate?TableName=Recipes',
        data: "",
        success: function(data) {
            json_data = data;
            console.log(json_data);
            populateTable();
        }
    });

function populateTable() {
    for (var i = 0; i < json_data.Count; i++) {
        var rName = json_data.Items[i].RecipeName;
        var rNameNoSpaces = rName.replace(/\s/g, '');
        // recipes_ARRAY[i] = rName;
        // imageURL_DICT.rName = json_data.Items[i].Ingredients;
        // ingredients_DICT.rName = json_data.Items[i].Directions;
        // directions_DICT.rName = json_data.Items[i].ImageURL;
        console.log(json_data.Items[i].Ingredients);

        var tableItemHTML =  "\
                          <div class=\"col-md-4 col-sm-6 portfolio-item\"> \
                              <a href=\"#portfolioModal" + rNameNoSpaces + "\" class=\"portfolio-link\" data-toggle=\"modal\"> \
                                  <div class=\"portfolio-hover\"> \
                                      <div class=\"portfolio-hover-content\"> \
                                          <i class=\"fa fa-plus fa-3x\"></i> \
                                      </div> \
                                  </div> \
                                  <img src=" + json_data.Items[i].ImageURL + " class=\"img-responsive\" alt=\"\"> \
                              </a> \
                              <div class=\"portfolio-caption\"> \
                                  <h4>" + rName + "</h4> \
                                  <a href=\"#portfolioModal1\" class=\"portfolio-link\" data-toggle=\"modal\">Click for ingredients</a> \
                              </div> \
                          </div>";
        $("#recipeTable").append(tableItemHTML);

        var recipeViewHTML = "\
                        <div class=\"portfolio-modal modal fade\" id=\"portfolioModal" + rNameNoSpaces + "\" tabindex=\"-1\" role=\"dialog\" aria-hidden=\"true\"> \
                            <div class=\"modal-dialog\"> \
                                <div class=\"modal-content\"> \
                                    <div class=\"close-modal\" data-dismiss=\"modal\"> \
                                        <div class=\"lr\"> \
                                            <div class=\"rl\"> \
                                            </div> \
                                        </div> \
                                    </div> \
                                    <div class=\"container\"> \
                                        <div class=\"row\"> \
                                            <div class=\"col-lg-8 col-lg-offset-2\"> \
                                                <div class=\"modal-body\"> \
                                                    <h2>Recipe Directions for...</h2> \
                                                    <p class=\"item-intro text-muted\">" + rName + "</p> \
                                                    <img class=\"img-responsive img-centered\" src=" + json_data.Items[i].ImageURL + " width=\"200\" height=\"40\" alt=\"\"> \
                                                    <div>" + json_data.Items[i].Directions.replace(/\n/g,"<br>") + "</div> \
                                                    <p> \
                                                        <b>Ingredients </b> \
                                                    </p> \
                                                    <p class=ingredients-list>" + json_data.Items[i].Ingredients.replace(/\n/g,"<br>") + "</p> \
                                                    <button type=\"button\" class=\"btn btn-primary\" data-dismiss=\"modal\"><i class=\"fa fa-times\"></i> Home</button> \
                                                    <button type=\"button\" class=\"btn btn-primary\" data-dismiss=\"modal\"><i class=\"fa fa-times\"></i> Search</button> \
                                                    <button type=\"button\" class=\"btn btn-primary\" data-dismiss=\"modal\"><i class=\"fa fa-times\"></i> Back</button> \
                                                </div> \
                                            </div> \
                                        </div> \
                                    </div> \
                                </div> \
                            </div> \
                        </div>";
        $("#recipe-view").append(recipeViewHTML);
    }
}
    // var recipeItem;
    // var i = 0;
    // // for (recipeItem in json_data.Items) {
    // //     //modal i recipeTitle = recipeItem.RecipeName;
    // //     //modal i directions = recipeItem.Directions;
    // //     //modal i imgURL = recipeItem.imgURL
    // //     //modal i ingredients = recipeItem.Ingredients;
    // // }
    // $("#recipeTable").append(portfolioItemHTML);
});
