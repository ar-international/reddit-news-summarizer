import React from 'react';

const NewsTile = ({ item }) => {
    return (
        <div className="news-tile">
            <div className="rank">#{item.rank}</div>
            <h3>
                <a href={item.url} target="_blank" rel="noopener noreferrer">
                    {item.title}
                </a>
            </h3>
            <p>{item.explanation}</p>
        </div>
    );
};

export default NewsTile;
