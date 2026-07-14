/**
 * Reusable Pagination Component
 */

import "./Pagination.css";

function Pagination({

    currentPage,

    totalItems,

    itemsPerPage,

    onPageChange,

    onItemsPerPageChange

}) {

    const totalPages = Math.ceil(

        totalItems / itemsPerPage

    );

    if (totalPages <= 1) {

        return null;

    }

    return (

        <div className="pagination-container">

            <div className="pagination-left">

                <span>

                    Show

                </span>

                <select

                    value={itemsPerPage}

                    onChange={(event) =>

                        onItemsPerPageChange(

                            Number(

                                event.target.value

                            )

                        )

                    }

                >

                    <option value={5}>5</option>

                    <option value={10}>10</option>

                    <option value={20}>20</option>

                </select>

                <span>

                    entries

                </span>

            </div>

            <div className="pagination-right">

                <button

                    disabled={

                        currentPage === 1

                    }

                    onClick={() =>

                        onPageChange(

                            currentPage - 1

                        )

                    }

                >

                    Previous

                </button>

                {

                    [...Array(totalPages)].map(

                        (_, index) => (

                            <button

                                key={index}

                                className={

                                    currentPage === index + 1

                                    ?

                                    "active-page"

                                    :

                                    ""

                                }

                                onClick={() =>

                                    onPageChange(

                                        index + 1

                                    )

                                }

                            >

                                {

                                    index + 1

                                }

                            </button>

                        )

                    )

                }

                <button

                    disabled={

                        currentPage === totalPages

                    }

                    onClick={() =>

                        onPageChange(

                            currentPage + 1

                        )

                    }

                >

                    Next

                </button>

            </div>

        </div>

    );

}

export default Pagination;