/**
 * Category Card
 *
 * Responsibilities:
 * - Display category information
 * - Show total assessments (future)
 * - Reusable dashboard component
 */

import {
    FaFolderOpen
} from "react-icons/fa";

import "./CategoryCard.css";

function CategoryCard({

    name,

    description

}) {

    return (

        <div className="category-card">

            <div className="category-icon">

                <FaFolderOpen />

            </div>

            <div className="category-details">

                <h3>

                    {name}

                </h3>

                <p>

                    {description}

                </p>

            </div>

        </div>

    );

}

export default CategoryCard;