USE retail_pos;

-- 1. Turn off Safe Update Mode temporarily
SET SQL_SAFE_UPDATES = 0;

-- 2. Update your existing items with the images
UPDATE products SET image_url = 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400&q=80' WHERE product_name LIKE '%Mouse%';
UPDATE products SET image_url = 'https://rukminim2.flixcart.com/image/480/640/jievpu80/paper/y/y/s/paper-a4-paper-jk-paper-original-imaewxdvxypguw5h.jpeg?q=90' WHERE product_name LIKE '%Paper%';
UPDATE products SET image_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQuqdC99uuX35ulzFgRUd0iZY6w-KN2jNov8g&s' WHERE product_name LIKE '%Cable%';

-- 3. Turn Safe Update Mode back on for safety
SET SQL_SAFE_UPDATES = 1;
USE retail_pos;
SET SQL_SAFE_UPDATES = 0;

-- Add an image for the Pens
UPDATE products SET image_url = 'https://images.unsplash.com/photo-1585336261022-680e295ce3fe?w=400&q=80' WHERE product_name LIKE '%Pen%';

-- Add an image for the Chips
UPDATE products SET image_url = 'https://instamart-media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto/NI_CATALOG/IMAGES/CIW/2026/2/18/638a94be-069d-40c8-9683-0c0dc05bb3ff_15290_1.png' WHERE product_name LIKE '%Chips%';

SET SQL_SAFE_UPDATES = 1;