/*
 * Copyright (c) 2024.
 * Autheur : Adrien JAUFRE
 */

package fr.cpe.emergencymanager.Repository;

import fr.cpe.emergencymanager.Entities.Parameter;

public class ParameterRepository extends Repository<Parameter> {
    public ParameterRepository() {
        setEndpoint(Parameter.ENDPOINT);
        setType(Parameter.class);
    }
}
