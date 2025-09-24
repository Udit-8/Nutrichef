# 🤖 Nutrition Chatbot - JSON-Based Data Structure & Attributes

## **Overview**
This document outlines the data structure and attributes optimized for JSON file-based storage instead of database or external API integration. All data will be stored in structured JSON files that the chatbot reads and updates locally.

---

## **Core JSON File Structure**

### **Main Data Files:**
1. `recipes.json` - All recipe data
2. `foods_nutrition.json` - Food nutritional database
3. `user_profiles.json` - User preferences and profiles
4. `meal_plans.json` - Saved meal plans
5. `grocery_lists.json` - Saved grocery lists
6. `food_logs.json` - User food tracking data
7. `session_data.json` - Current session state
8. `app_settings.json` - Global app configuration

---

## **Journey 1: Recipe Discovery**

### **recipes.json Structure:**
```json
{
  "recipes": [
    {
      "id": "recipe_001",
      "name": "Chicken Stir Fry",
      "image": "images/chicken_stir_fry.jpg",
      "cuisine": "asian",
      "difficulty": "easy",
      "prep_time": 15,
      "cook_time": 10,
      "total_time": 25,
      "servings": 4,
      "rating": 4.5,
      "rating_count": 127,
      "description": "Quick and healthy chicken stir fry",
      "tags": ["quick", "healthy", "family_friendly"],
      "occasions": ["weeknight_dinner", "quick_lunch"],
      "dietary_tags": ["gluten_free", "dairy_free"],
      "ingredients": [
        {
          "name": "chicken breast",
          "amount": 1,
          "unit": "lb",
          "category": "protein"
        }
      ],
      "instructions": [
        {
          "step": 1,
          "instruction": "Cut chicken into strips",
          "time": 5,
          "tips": "Cut against the grain"
        }
      ],
      "nutrition_per_serving": {
        "calories": 285,
        "protein": 28,
        "carbs": 12,
        "fat": 14,
        "fiber": 3
      },
      "equipment": ["wok", "cutting_board", "knife"]
    }
  ],
  "cuisines": ["asian", "italian", "mexican", "american", "indian"],
  "dietary_options": ["vegetarian", "vegan", "gluten_free", "dairy_free", "keto"],
  "occasions": ["weeknight_dinner", "party", "quick_lunch", "meal_prep"]
}
```

### **Recipe Discovery Session Attributes:**
```json
{
  "discovery_session": {
    "method": "cuisine|ingredients|dietary|time|occasion",
    "preferences": {
      "selected_cuisine": "asian",
      "available_ingredients": ["chicken", "vegetables"],
      "dietary_restrictions": ["gluten_free"],
      "max_cook_time": 30,
      "occasion": "weeknight_dinner"
    },
    "search_results": ["recipe_001", "recipe_002"],
    "current_page": 1,
    "results_per_page": 5
  }
}
```

---

## **Journey 2: Step-by-Step Cooking Guidance**

### **Cooking Session Structure (session_data.json):**
```json
{
  "cooking_sessions": {
    "session_001": {
      "recipe_id": "recipe_001",
      "status": "active|paused|completed",
      "servings": 4,
      "start_time": "2024-01-15T18:30:00Z",
      "current_step": 3,
      "total_steps": 8,
      "completed_steps": [1, 2],
      "active_timers": [
        {
          "name": "cook_chicken",
          "duration": 300,
          "remaining": 180,
          "started_at": "2024-01-15T18:35:00Z"
        }
      ],
      "phase": "prep|cooking|serving",
      "voice_mode": true,
      "user_notes": "Added extra garlic",
      "scaled_ingredients": [
        {
          "name": "chicken breast",
          "original_amount": 1,
          "scaled_amount": 1,
          "unit": "lb"
        }
      ]
    }
  }
}
```

---

## **Journey 3: Calorie-Based Meal Suggestions**

### **Meal Suggestions Structure:**
```json
{
  "meal_suggestions": {
    "calorie_targets": {
      "300": ["meal_001", "meal_002"],
      "500": ["meal_003", "meal_004"],
      "700": ["meal_005", "meal_006"]
    },
    "meals": [
      {
        "id": "meal_001",
        "name": "Greek Salad with Chicken",
        "image": "images/greek_salad.jpg",
        "calories": 295,
        "prep_time": 15,
        "meal_type": ["lunch", "dinner"],
        "macros": {
          "protein": 25,
          "carbs": 15,
          "fat": 18,
          "fiber": 8
        },
        "components": [
          {
            "food_id": "food_001",
            "name": "grilled chicken",
            "amount": 100,
            "unit": "g"
          }
        ],
        "dietary_tags": ["gluten_free", "keto_friendly"],
        "substitutions": [
          {
            "original": "chicken",
            "alternatives": ["tofu", "chickpeas", "salmon"]
          }
        ]
      }
    ]
  }
}
```

### **User Calorie Session:**
```json
{
  "calorie_session": {
    "target_calories": 500,
    "timeframe": "single_meal|daily|weekly",
    "meal_type": "lunch",
    "preferences": {
      "dietary_restrictions": ["vegetarian"],
      "cuisines": ["mediterranean", "asian"],
      "dislikes": ["mushrooms"],
      "allergies": ["nuts"]
    },
    "generated_suggestions": ["meal_001", "meal_003"],
    "selected_meals": ["meal_001"],
    "customizations": [
      {
        "meal_id": "meal_001",
        "changes": "removed_feta_cheese",
        "new_calories": 250
      }
    ]
  }
}
```

---

## **Journey 4: Event-Driven Meal Planning**

### **Event Planning Structure:**
```json
{
  "events": [
    {
      "id": "event_001",
      "name": "Birthday Party",
      "type": "birthday",
      "date": "2024-02-15",
      "start_time": "18:00",
      "duration": 4,
      "guest_count": 12,
      "venue": "home",
      "budget": {
        "min": 150,
        "max": 300,
        "currency": "USD"
      },
      "constraints": {
        "kitchen_size": "medium",
        "equipment": ["oven", "stovetop", "grill"],
        "prep_time_available": 240
      },
      "preferences": {
        "service_style": "buffet",
        "cuisines": ["italian", "american"],
        "dietary_accommodations": ["vegetarian_option", "gluten_free_option"],
        "kids_menu": true
      },
      "menu": {
        "appetizers": ["app_001", "app_002"],
        "mains": ["main_001"],
        "sides": ["side_001", "side_002"],
        "desserts": ["dessert_001"]
      },
      "shopping_list": ["ingredient_001", "ingredient_002"],
      "prep_schedule": [
        {
          "task": "prep_vegetables",
          "start_time": "2024-02-15T14:00:00Z",
          "duration": 30
        }
      ],
      "cost_breakdown": {
        "appetizers": 45,
        "mains": 120,
        "sides": 30,
        "desserts": 25,
        "total": 220
      }
    }
  ]
}
```

---

## **Journey 5: Daily and Weekly Meal Planning**

### **meal_plans.json Structure:**
```json
{
  "meal_plans": [
    {
      "id": "plan_001",
      "name": "Weekly Meal Plan - Week 1",
      "type": "weekly",
      "start_date": "2024-01-15",
      "end_date": "2024-01-21",
      "user_id": "user_001",
      "target_calories_per_day": 2000,
      "target_macros_per_day": {
        "protein": 150,
        "carbs": 200,
        "fat": 89
      },
      "household_size": 2,
      "meals_included": ["breakfast", "lunch", "dinner"],
      "daily_plans": [
        {
          "date": "2024-01-15",
          "breakfast": {
            "recipe_id": "recipe_010",
            "servings": 2,
            "calories": 350,
            "prep_time": 10
          },
          "lunch": {
            "recipe_id": "recipe_020",
            "servings": 2,
            "calories": 450,
            "prep_time": 15
          },
          "dinner": {
            "recipe_id": "recipe_030",
            "servings": 2,
            "calories": 650,
            "prep_time": 30
          },
          "daily_totals": {
            "calories": 1450,
            "protein": 120,
            "carbs": 150,
            "fat": 65
          }
        }
      ],
      "grocery_list_id": "grocery_001",
      "customizations": [
        {
          "date": "2024-01-16",
          "meal": "dinner",
          "original_recipe": "recipe_040",
          "new_recipe": "recipe_041",
          "reason": "user_preference"
        }
      ],
      "leftover_planning": [
        {
          "original_date": "2024-01-15",
          "original_meal": "dinner",
          "reuse_date": "2024-01-16",
          "reuse_meal": "lunch"
        }
      ]
    }
  ],
  "meal_plan_templates": [
    {
      "id": "template_001",
      "name": "Vegetarian Weekly",
      "description": "Plant-based meals for the week",
      "target_calories": 1800,
      "dietary_tags": ["vegetarian"]
    }
  ]
}
```

---

## **Journey 6: Food and Calorie Tracking**

### **foods_nutrition.json Structure:**
```json
{
  "foods": [
    {
      "id": "food_001",
      "name": "Chicken Breast, Grilled",
      "brand": null,
      "category": "protein",
      "barcode": null,
      "serving_options": [
        {
          "size": "100g",
          "calories": 165,
          "macros": {
            "protein": 31,
            "carbs": 0,
            "fat": 3.6,
            "fiber": 0
          }
        },
        {
          "size": "1 piece (85g)",
          "calories": 140,
          "macros": {
            "protein": 26,
            "carbs": 0,
            "fat": 3.1,
            "fiber": 0
          }
        }
      ],
      "micronutrients_per_100g": {
        "vitamin_b6": 0.9,
        "niacin": 14.8,
        "phosphorus": 220,
        "selenium": 27.6
      },
      "tags": ["high_protein", "low_carb"]
    }
  ],
  "food_categories": ["protein", "carbs", "vegetables", "fruits", "dairy", "fats"],
  "common_serving_sizes": {
    "protein": ["100g", "1 piece", "1 serving"],
    "vegetables": ["1 cup", "100g", "1 piece"],
    "fruits": ["1 medium", "1 cup", "100g"]
  }
}
```

### **food_logs.json Structure:**
```json
{
  "food_logs": [
    {
      "user_id": "user_001",
      "date": "2024-01-15",
      "entries": [
        {
          "id": "entry_001",
          "food_id": "food_001",
          "meal_type": "lunch",
          "quantity": 150,
          "unit": "g",
          "logged_at": "2024-01-15T12:30:00Z",
          "method": "search",
          "calories": 248,
          "macros": {
            "protein": 46.5,
            "carbs": 0,
            "fat": 5.4,
            "fiber": 0
          }
        }
      ],
      "daily_totals": {
        "calories": 1850,
        "protein": 140,
        "carbs": 180,
        "fat": 70,
        "fiber": 25
      },
      "daily_goals": {
        "calories": 2000,
        "protein": 150,
        "carbs": 200,
        "fat": 89
      },
      "meal_breakdown": {
        "breakfast": {"calories": 400, "protein": 20},
        "lunch": {"calories": 500, "protein": 35},
        "dinner": {"calories": 650, "protein": 45},
        "snacks": {"calories": 300, "protein": 40}
      }
    }
  ],
  "weekly_summaries": [
    {
      "user_id": "user_001",
      "week_start": "2024-01-15",
      "average_daily_calories": 1920,
      "goal_adherence": 85,
      "streak_days": 5
    }
  ]
}
```

---

## **Journey 7: Grocery Assistance**

### **grocery_lists.json Structure:**
```json
{
  "grocery_lists": [
    {
      "id": "grocery_001",
      "name": "Weekly Shopping - Jan 15",
      "user_id": "user_001",
      "created_at": "2024-01-15T08:00:00Z",
      "last_modified": "2024-01-15T10:30:00Z",
      "source": "meal_plan",
      "source_ids": ["plan_001"],
      "status": "active",
      "items": [
        {
          "id": "item_001",
          "name": "Chicken Breast",
          "quantity": 2,
          "unit": "lbs",
          "category": "protein",
          "aisle": 8,
          "estimated_cost": 12.99,
          "brand_preference": null,
          "priority": "essential",
          "status": "pending",
          "notes": "organic if available",
          "substitutions": ["chicken thighs", "turkey breast"]
        }
      ],
      "store_sections": {
        "produce": ["item_002", "item_003"],
        "dairy": ["item_004"],
        "meat": ["item_001"],
        "pantry": ["item_005", "item_006"]
      },
      "total_estimated_cost": 85.43,
      "shared_with": ["user_002"],
      "export_history": [
        {
          "format": "email",
          "sent_to": "user@example.com",
          "sent_at": "2024-01-15T09:00:00Z"
        }
      ]
    }
  ],
  "consolidation_rules": {
    "combine_similar": true,
    "unit_conversions": {
      "milk": {"1 gallon": "4 quarts", "1 quart": "2 pints"}
    }
  },
  "store_layouts": [
    {
      "store_name": "Default Store",
      "sections": [
        {"name": "produce", "aisle": [1, 2]},
        {"name": "dairy", "aisle": [3]},
        {"name": "meat", "aisle": [8, 9]}
      ]
    }
  ]
}
```

---

## **Journey 8: Nutritional Food Profile**

### **Enhanced foods_nutrition.json for Detailed Lookup:**
```json
{
  "detailed_foods": [
    {
      "id": "food_detail_001",
      "name": "Salmon, Atlantic, Farmed",
      "scientific_name": "Salmo salar",
      "category": "fish",
      "subcategory": "fatty_fish",
      "preparation": "raw",
      "per_100g": {
        "calories": 208,
        "macros": {
          "protein": 25.4,
          "total_carbs": 0,
          "dietary_fiber": 0,
          "sugars": 0,
          "total_fat": 12.4,
          "saturated_fat": 3.05,
          "trans_fat": 0,
          "cholesterol": 59,
          "sodium": 44
        },
        "vitamins": {
          "vitamin_a": 58,
          "vitamin_c": 0,
          "vitamin_d": 11,
          "vitamin_e": 3.55,
          "vitamin_k": 0.1,
          "thiamine": 0.226,
          "riboflavin": 0.155,
          "niacin": 8.042,
          "vitamin_b6": 0.636,
          "folate": 26,
          "vitamin_b12": 3.05
        },
        "minerals": {
          "calcium": 9,
          "iron": 0.34,
          "magnesium": 28,
          "phosphorus": 240,
          "potassium": 384,
          "zinc": 0.64,
          "copper": 0.087,
          "manganese": 0.016,
          "selenium": 36.5
        },
        "fatty_acids": {
          "omega_3_total": 2.018,
          "dha": 1.104,
          "epa": 0.690,
          "omega_6_total": 0.341
        }
      },
      "health_benefits": [
        "high_in_omega_3",
        "good_source_protein",
        "vitamin_d_source"
      ],
      "allergen_info": ["fish"],
      "storage_tips": "Keep refrigerated, use within 2 days",
      "seasonal_availability": "year_round",
      "sustainability_rating": "moderate",
      "data_source": "USDA_SR",
      "last_updated": "2024-01-01",
      "similar_foods": ["food_detail_002", "food_detail_003"],
      "healthier_alternatives": ["food_detail_004"]
    }
  ],
  "comparison_data": {
    "protein_sources": {
      "high_protein_foods": ["food_detail_001", "food_detail_005"],
      "complete_proteins": ["food_detail_001", "food_detail_006"]
    }
  }
}
```

---

## **Cross-Journey Data Files**

### **user_profiles.json:**
```json
{
  "users": [
    {
      "id": "user_001",
      "profile": {
        "dietary_restrictions": ["gluten_free"],
        "food_allergies": ["nuts"],
        "cuisine_preferences": ["mediterranean", "asian"],
        "cooking_skill": "intermediate",
        "daily_calorie_goal": 2000,
        "macro_ratios": {
          "protein": 30,
          "carbs": 40,
          "fat": 30
        },
        "ingredient_dislikes": ["mushrooms", "olives"],
        "kitchen_equipment": ["oven", "stovetop", "blender", "food_processor"],
        "household_size": 2,
        "budget_per_day": 25,
        "measurement_preference": "metric"
      },
      "favorites": {
        "recipes": ["recipe_001", "recipe_010"],
        "foods": ["food_001", "food_005"],
        "meal_plans": ["plan_001"]
      },
      "frequently_used": {
        "recent_foods": ["food_001", "food_002", "food_003"],
        "recent_recipes": ["recipe_001", "recipe_002"]
      },
      "achievements": {
        "recipes_cooked": 25,
        "days_tracked": 45,
        "streak_best": 12
      }
    }
  ]
}
```

### **session_data.json:**
```json
{
  "current_session": {
    "session_id": "session_001",
    "user_id": "user_001",
    "start_time": "2024-01-15T09:00:00Z",
    "current_journey": "recipe_discovery",
    "journey_history": ["recipe_discovery", "cooking_guidance"],
    "conversation_context": {
      "last_intent": "find_recipe",
      "entities": {
        "cuisine": "italian",
        "time_constraint": 30
      }
    },
    "temporary_data": {
      "search_results": ["recipe_001", "recipe_002"],
      "current_recipe": "recipe_001",
      "journey_specific": {}
    }
  }
}
```

### **app_settings.json:**
```json
{
  "settings": {
    "version": "1.0.0",
    "default_serving_size": 1,
    "supported_units": ["metric", "imperial"],
    "default_currency": "USD",
    "max_search_results": 10,
    "session_timeout": 3600,
    "data_retention_days": 365,
    "backup_frequency": "daily"
  },
  "feature_flags": {
    "voice_commands": true,
    "barcode_scanning": false,
    "meal_plan_export": true,
    "grocery_delivery_integration": false
  }
}
```

---

## **Key Changes for JSON Implementation**

### **1. Data Structure Optimization:**
- Flattened nested relationships for easier JSON parsing
- Added explicit ID references instead of foreign keys
- Simplified array structures for better performance
- Pre-calculated common values to reduce computation

### **2. File Organization:**
- Separated data by functionality for better file management
- Kept related data together to minimize file reads
- Added indexes for common queries
- Implemented data redundancy for performance

### **3. Session Management:**
- Lightweight session storage in JSON
- Temporary data separation from permanent data
- Easy serialization/deserialization
- State persistence across app restarts

### **4. Search and Filtering:**
- Pre-built search indexes in JSON structure
- Tag-based filtering systems
- Category hierarchies for quick lookup
- Cached common queries

### **5. Data Consistency:**
- Standardized data formats across all files
- Consistent ID naming conventions
- Unified date/time formats (ISO 8601)
- Standardized units and measurements

This JSON-based approach provides a complete, self-contained data structure that can run independently without external dependencies while maintaining all the functionality of the original attribute design.