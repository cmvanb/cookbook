function ErrorCard({ message, detail, renderHelp }) {
    return (
        <>
            <article class='border error-container'>
                <h6>{message}</h6>
                {renderHelp && renderHelp()}
                {detail && (
                    <pre class='error-detail'>
                        {JSON.stringify(detail, null, 2)}
                    </pre>
                )}
            </article>
            <br />
        </>
    )
}

export default ErrorCard
