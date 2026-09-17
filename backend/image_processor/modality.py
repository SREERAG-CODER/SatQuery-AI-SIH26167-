def identify_modality(metadata):

    evidence = []

    tags = metadata["tags"]

    for key, value in tags.items():

        text = f"{key} {value}".lower()

        if any(word in text for word in [
            "sentinel-1",
            "sar",
            "sigma0",
            "gamma0",
            "backscatter"
        ]):
            evidence.append(f"SAR clue: {key} = {value}")

        if any(word in text for word in [
            "sentinel-2",
            "multispectral",
            "optical"
        ]):
            evidence.append(f"Optical clue: {key} = {value}")

    for band in metadata["bands"]:

        description = band["description"].lower()

        if any(word in description for word in [
            "sentinel-1",
            "sar",
            "sigma0",
            "gamma0",
            "backscatter",
            "vv",
            "vh",
            "hh",
            "hv"
        ]):
            evidence.append(
                f"SAR band clue: {band['description']}"
            )

        if any(word in description for word in [
            "red",
            "green",
            "blue",
            "nir",
            "swir",
            "red edge"
        ]):
            evidence.append(
                f"Optical band clue: {band['description']}"
            )

    sar_evidence = [
        item for item in evidence
        if "SAR" in item
    ]

    optical_evidence = [
        item for item in evidence
        if "Optical" in item
    ]

    if sar_evidence and not optical_evidence:
        return {
            "modality": "SAR",
            "confidence": "high",
            "evidence": evidence
        }

    if optical_evidence and not sar_evidence:
        return {
            "modality": "OPTICAL",
            "confidence": "high",
            "evidence": evidence
        }

    return {
        "modality": "UNKNOWN",
        "confidence": "low",
        "evidence": [
            "Metadata does not provide convincing modality information."
        ]
    }