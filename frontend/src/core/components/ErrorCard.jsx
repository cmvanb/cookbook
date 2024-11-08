function ErrorCard({ message, details, renderHelp }) {
    return (
        <>
            <article class='border error-container'>
                <h6>{message}</h6>
                {renderHelp && renderHelp()}
                {details && (
                    <pre class='error-detail'>
                        {JSON.stringify(details, null, 2)}
                    </pre>
                )}
            </article>
            <br />
        </>
    )
}

export default ErrorCard
