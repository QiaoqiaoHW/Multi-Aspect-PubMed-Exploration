import json

######
# get colors for all the clusters
######
palette_colors = ['#246b9e', '#3b528b', '#45818e', '#53a57d', '#5d9346', 
                  '#71b978', '#93c47d', '#9ce6e1', '#9df57d', '#9fc5e8', 
                  '#a9b5ef', '#abc0d6', '#abc3cc', '#abd6c5', '#b5e4a0', 
                  '#c3e1e7', '#c96552', '#c991b5', '#ca76bc', '#cdf2f0', 
                  '#cefabe', '#d0f867', '#e48bba', '#e7cba9', '#e7cba9',
                  '#e8ad46', '#eeeeee', '#ef6578', '#ef7b9f', '#f0ebb2', 
                  '#f1dcaa', '#f3d6a3', '#f3e86e', '#f3fdd9', '#f4987a', 
                  '#f5a8d1', '#faa0a0', '#fbd8dd']
labels = [i for i in range(38)]

colors_new_legend = dict(zip(labels, palette_colors))

######
# get topics for all the clusters
######
# with open("../configure/topic_labels.json", "r") as f:
#     topic_labels = json.load(f)

topic_labels = [{"label": 0, "category": "chemistry_material_physics"}, {"label": 1, "category": "environment_neurology_psychiatry"}, {"label": 2, "category": "surgery_material_pediatric"}, {"label": 3, "category": "environment_material_ecology"}, {"label": 4, "category": "cancer_immunology_pathology"}, 
                {"label": 5, "category": "rehabilitation_neurology_engineering"}, {"label": 6, "category": "microbiology_infectious_immunology"}, {"label": 7, "category": "psychology_psychiatry_nursing"}, {"label": 8, "category": "material_chemistry_physics"}, {"label": 9, "category": "nutrition_cardiology_pediatric"}, 
                {"label": 10, "category": "surgery_pediatric_radiology"}, {"label": 11, "category": "environment_chemistry_material"}, {"label": 12, "category": "cardiology_neuroscience_dermatology"}, {"label": 13, "category": "veterinary_infectious_virology"}, {"label": 14, "category": "pharmacology_chemistry_nutrition"}, 
                {"label": 15, "category": "surgery_cardiology_radiology"}, {"label": 16, "category": "chemistry_genetics_biochemistry"}, {"label": 17, "category": "neuroscience_psychiatry_psychology"}, {"label": 18, "category": "gynecology_pediatric_environment"}, {"label": 19, "category": "surgery_rehabilitation_veterinary"}, 
                {"label": 20, "category": "cancer_surgery_radiology"}, {"label": 21, "category": "genetics_neuroscience_neurology"}, {"label": 22, "category": "engineering_material_chemistry"}, {"label": 23, "category": "infectious_virology_chemistry"}, {"label": 24, "category": "ophthalmology_dermatology_immunology"}, 
                {"label": 25, "category": "chemistry_material_environment"}, {"label": 26, "category": "cancer_chemistry_pharmacology"}, {"label": 27, "category": "nursing_education_surgery"}, {"label": 28, "category": "ecology_environment_physiology"}, {"label": 29, "category": "optics_engineering_physics"}, 
                {"label": 30, "category": "environment_biochemistry_physiology"}, {"label": 31, "category": "immunology_pharmacology_chemistry"}, {"label": 32, "category": "chemistry_microbiology_biochemistry"}, {"label": 33, "category": "physics_optics_chemistry"}, {"label": 34, "category": "nutrition_education_nursing"}, 
                {"label": 35, "category": "environment_microbiology_material"}, {"label": 36, "category": "chemistry_bioinformatics_biochemistry"}, {"label": 37, "category": "surgery_pediatric_nursing"}]



topics = []
labels = []
for item in topic_labels:
    topics.append(item["category"])
    labels.append(item["label"])

topics_new_legend = dict(zip(labels,topics))
